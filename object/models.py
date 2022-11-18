# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from bucket.models import Bucket

class Object(models.Model):
    id = models.BigAutoField(primary_key=True)
    # aws fields
    lastmodified = models.CharField(u'LastModified', max_length=255, blank=False, null=False)
    etag = models.CharField(u'ETag', max_length=255, blank=False, null=False, unique=True)
    storageclass = models.CharField(u'StorageClass', max_length=1024, blank=False, null=False)
    key = models.CharField(u'Key', max_length=1024, blank=False, null=False)
    size = models.CharField(u'Size', max_length=1024, blank=False, null=False)
    owner_display_name = models.CharField(u'Owner', max_length=1024, blank=False, null=False)
    owner_id = models.CharField(u'Owner ID', max_length=1024, blank=False, null=False)

    # custom
    bucket = models.ForeignKey(Bucket, null=False, blank=False, on_delete=models.RESTRICT)
    key_extension = models.CharField(u'Format', max_length=255, blank=True, null=True)
    key_level = models.IntegerField(u'Key level', default=0)
    size_easy = models.CharField(u'Size-Easy', max_length=255, blank=True, null=True)
    compress_content = models.TextField(u'Content', blank=True, null=True)

    # auditory
    date_join = models.DateTimeField('Date created', default=timezone.now, blank=False, null=False)
    date_update = models.DateTimeField('Date updated', default=timezone.now, blank=True, null=True)

    def __str__(self):
        return u"%s" % (self.id)

    class Meta:
        ordering = ['key']
        verbose_name = ('Object')
        verbose_name_plural = ('Objects')

    def save(self, *args, **kargs):
        '''
        key level
        return tree level number of key
        s3://bucket-name/teste-lixo-apagar/zip-teste-30-nov-2021.zip
        self.key = teste-lixo-apagar/zip-teste-30-nov-2021.zip'
        ['teste-lixo-apagar', 'zip-teste-30-nov-2021.zip']
        return integer, 2 postions, 0 and 1
        '''
        if self.key:
            self.key_level = int(len(self.key.split('/')))

        super(Object, self).save()


    def get_split_(self):
        return self.key.split('/')


class Download(models.Model):
    id = models.UUIDField(u'ID', primary_key=True, unique=True, default=uuid.uuid4)
    date_join = models.DateTimeField('Date created', default=timezone.now, blank=False, null=False)
    user = models.OneToOneField(User, null=True, blank=True, verbose_name='Usuário', on_delete=models.RESTRICT)
    key = models.CharField(u'File', max_length=255, blank=False, null=False, help_text='S3path at bucket')
    content = models.TextField(u'Content', blank=True, null=True)
    url = models.CharField(u'Download URL', max_length=255, help_text="Public URL for download")
    expiry_link = models.DateTimeField('Expiry', default=timezone.now, blank=False, null=False)
    counter = models.IntegerField(u'Download Counter', default=0)

    def __str__(self):
        return u"%s" % self.id

    class Meta:
        ordering = ['date_join']
        verbose_name = ('Download')
        verbose_name_plural = ('Downloads')
