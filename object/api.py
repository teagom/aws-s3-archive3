# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from object.models import Object

def show_compress_content(request,obj_id,search):
    # open modal
    obj = Object.objects.get(pk=obj_id)
    template = loader.get_template('object/object_compress_content.html')
    content = []

    for x in obj.compress_content.split('\n'):
        content.append(x)

    context = {
        'request': request,
        'search': search,
        'obj': obj,
        'content': content
    }
    return HttpResponse(template.render(context, request))
