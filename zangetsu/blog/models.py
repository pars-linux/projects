# -*- coding: utf-8 -*-
from django.db import models

class Link(models.Model):

    title = models.CharField(maxlength = 64)
    url = models.URLField()

    def __str__(self):
        return self.title

    class Admin:
        list_display = ['title']

class Tag(models.Model):

    title = models.CharField(maxlength = 32)

    def __str__(self):
        return self.title

    class Admin:
        list_display = ('id', 'title')

class Entry(models.Model):

    title = models.CharField(maxlength = 256)
    content = models.TextField()
    tag = models.ManyToManyField(Tag)
    pubdate = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/%s/%s/' % (self.pubdate.strftime('%Y/%m/%d').lower(), self.id)

    class Meta:
        pass

    class Admin:
        list_display = ('id', 'title', 'pubdate')
        list_filter = ['pubdate']
        search_fields = ['title']
