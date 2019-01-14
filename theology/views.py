# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from theology import models
import datetime
# Create your views here.
def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色，宽，高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画面对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\AdobeArabic-Bold.otf', 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session,用于做进一步的验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def index(request):
    articles = models.Theologyarticles.articleObj.all()
    nowtime = datetime.datetime.now()
    return render(request,'index.html',{'articles':articles,'nowtime':nowtime})
def article_page(request):
    article_id = request.GET.get('article_id')
    if article_id == None:
        return HttpResponse(u'请求的文章不存在')
    try:
        article = models.Theologyarticles.articleObj.get(pk=article_id)
    except:
        return render(request,'404.html')
    else:
        return render(request,'article_page.html',{'article':article})
def article_edit_page(request, article_id):
    flag = request.session.get('flag', default=True)
    tips = ""
    if flag == False:
        tips = "Try again"
    request.session.clear()
    #str方法将参数转化为字符串，避免因传递类型差异引起的错误
    # -1代表是新增博客，否则是编辑博客，编辑博客时需要传递博客对象到页面并显示
    if str(article_id) == '0':
        return render(request, 'article_edit_page.html',{"tips":tips})
    article = models.Theologyarticles.articleObj.get(pk=article_id)
    return render(request, 'article_edit_page.html', {'article': article,"tips":tips})
def article_edit_page_action(request):
    title = request.POST.get('title', '默认标题')
    ##get是根据参数名称从form表单页获取内容
    content = request.POST.get('content', '默认内容')
    article_id = request.POST.get('article_id_hidden', 'ar')
    input_verifycode = request.POST.get('verifycode').upper()
    verifycode = request.session['verifycode'].upper()
    if input_verifycode != verifycode:
        print input_verifycode, verifycode
        request.session['flag'] = False
        return HttpResponseRedirect('/theology/article/edit/'+article_id)

    ##保存数据
    ##如果是0，标记新增，使用create方法，否则使用save方法
    ##新增是返回首页，编辑是返回详情页
    if str(article_id) == '0':
                article = models.Theologyarticles.articleObj.createTheologyariticle(title=title, content=content)
                #return HttpResponseRedirect("http://127.0.0.1:8000/theology/index/")
                return HttpResponseRedirect("/theology/index/")

    article = models.Theologyarticles.articleObj.updateTheologyarticle(article_id=article_id,title=title,content=content)
    return render(request, 'article_page.html', {'article': article})
def article_delete_action(request,article_id):
    models.Theologyarticles.articleObj.filter(id=article_id).update(isDelete='True')
    return HttpResponseRedirect("/theology/index/")
def verifycodefile(request):
    flag = request.session.get('flag',default=True)
    tips = ""
    if flag == False:
        tips = "Try again"
    request.session.clear()
    return render(request,'verifycodefile.html',{"tips":tips})
def verifycodecheck(request):
    input_verifycode = request.POST.get('verifycode').upper()
    verifycode = request.session['verifycode'].upper()
    if input_verifycode == verifycode :
        return HttpResponseRedirect('/theology/index')
    else:
        request.session["flag"] = False
        return HttpResponseRedirect('/theology/verifycodefile')
