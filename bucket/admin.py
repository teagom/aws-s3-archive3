# Register your models here.

from django.contrib import admin
from bucket.models import Bucket

class BucketAdmin(admin.ModelAdmin):
    list_display = ('id','name_short','name_aws')
    filter_horizontal = ('user',)
admin.site.register(Bucket, BucketAdmin)
