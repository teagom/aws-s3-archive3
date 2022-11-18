# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bucket(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_short = models.CharField(u'S3 name', max_length=255, blank=False, null=False)
    name_aws = models.CharField(u'Protocol+S3 name', max_length=255, blank=False, null=False, help_text='Full address of AWS S3:  s3://bucket-name')
    date_join = models.DateTimeField('Date created', default=timezone.now, blank=False, null=False)
    date_update = models.DateTimeField('Date updated', default=timezone.now, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name='Usuário')

    def __str__(self):
        return self.name_short

    class Meta:
        ordering = ['name_short']
        verbose_name = ('Bucket')
        verbose_name_plural = ('Buckets')
