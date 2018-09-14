# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TheologyarticlesManager(models.Manager):
    #add an article
    def createTheologyariticle(self, title,content,isDelete='False'):
        article = self.model()
        article.title = title
        article.content = content
        article.save()
        return article
    #update an article
    def updateTheologyarticle(self,article_id,title,content,isDelete='False'):
        article = self.get(pk=article_id)
        article.title = title
        article.content = content
        article.save()
        return article
    #get articles‘ list
    def all(self):
        # 默认查询未删除的信息
        # 调用父类的成员语法为：super().方法名
        return super(TheologyarticlesManager,self).all().filter(isDelete='False')

class Theologyarticles(models.Model):
    title = models.CharField(max_length=32, default='')
    # 文章正文，使用的是TextField
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    content = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add='True')
    last_modified_time = models.DateTimeField(auto_now='True')
    isDelete = models.BooleanField(default=False)
    articleObj = TheologyarticlesManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Theologyarticles"
        ordering = ['id']
