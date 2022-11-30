# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, sys
from uuid import uuid4
from archive import settings
from datetime import date, timedelta

from django.template import loader
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_protect

from object.models import Object, Download

import sys
sys.stdout = sys.stderr

def compress(request, days):
    '''
    request     request
    days        integer, days to expiry link
    return array
        d[0]    True (download object) | False
        d[1]    message, format html
    '''
    # download
    tmp_filename = u"%s.zip" % uuid4()
    tmp_foldername = u"%s" % uuid4()
    tmp_folder = '%s/%s' % (settings.TEMPORARY_DS_ROOT, tmp_foldername)
    cmd = 'mkdir -p %s' % tmp_folder
    os.system(cmd)
    dwn_content = '' # conteudo do download, zip.
    dwn_zip_file = "%s/%s" % (tmp_folder, tmp_filename)

    if request.session['my_selected_objs']:
        dwn_content += u"Days to expiry %s\n" % days

        for x in request.session['my_selected_objs']:
            obj = Object.objects.get(pk=x)

            # get level key of selected object
            n = int(request.POST.get('object%s' % x))
            # build path selected level
            c = 0
            while c < n:
                try:
                    key_level += '/%s' %  obj.key.split('/')[c]
                except:
                    key_level = '/%s' %  obj.key.split('/')[c]
                c += 1

            src_file = u"%s%s" % (obj.bucket.name_aws, key_level)
            # copy
            cmd = u"/usr/local/bin/aws s3 cp %s %s%s" % (src_file, tmp_folder, key_level)
            r = os.system(cmd)
            if int(r) != 0:
                print('ERRO! Copying file from %s' % src_file)

            # copy recursive
            cmd = u"/usr/local/bin/aws s3 cp --recursive %s %s%s" % (src_file, tmp_folder, key_level)
            r = os.system(cmd)
            if int(r) != 0:
                print('ERRO! Copying file from %s' % src_file)

            dwn_content += u"%s\n" % src_file
            del(key_level)

        # compress zip
        cmd = "/usr/bin/zip -9r %s %s" % (dwn_zip_file, tmp_folder)
        os.system(cmd)

        # s3://<bucket>/folder/file.zip
        bucket_dest = u"%s/%s/%s" % (settings.AWS_BUCKET_S3, tmp_foldername, tmp_filename)
        cmd = "/usr/local/bin/aws s3 cp %s %s" % (dwn_zip_file, bucket_dest)
        os.system(cmd)

        # delete tmp folder and content
        # talvez seja criado dentro do caminho, updatedb não encontra, usar find . -name file.zip
        # /tmp/systemd-private-xyz-apache2.service/tmp/archive/temporary/<folder>/<file>.zip
        # delete tmp file
        #cmd = "rm %s" % dwn_zip_file
        #os.system(cmd)
        # delete tmp folder and content
        #cmd = 'rm -rf %s' % tmp_folder
        #os.system(cmd)

        # set public
        key = "%s/%s" % (tmp_foldername, tmp_filename)
        cmd = "/usr/local/bin/aws s3api put-object-acl --bucket %s --key %s --acl public-read" % (settings.AWS_BUCKET, key)
        os.system(cmd)

        # new download
        d = Download()
        d.user = request.user
        d.url = "%s/%s" % (settings.AWS_BUCKET_URL, key)
        d.key = "%s/%s" % (settings.AWS_BUCKET_S3, key)
        d.content = dwn_content
        d.expiry_link = date.today() + timedelta(days)
        d.save()

        link = format_html('<a target="_blank" href="{}">Download {} </a>', d.url, d.url)

        # clean my selected objects
        del request.session['my_selected_objs']
        start_session(request)
    else:
        d = False
        link = format_html('Sua lista de objectos está vazia!')

    return [d, link]


# options actions
def compress3(request):
    d = compress(request, 3)
    if d[0]:
        messages.add_message(request, messages.SUCCESS, d[1])
    else:
        messages.add_message(request, messages.ERROR, d[1])

def compress7(request, queryset):
    d = compress(request, 7)
    if d[0]:
        messages.add_message(request, messages.SUCCESS, d[1])
    else:
        messages.add_message(request, messages.ERROR, d[1])

def compress10(request, queryset):
    d = compress(request, 10)
    if d[0]:
        messages.add_message(request, messages.SUCCESS, d[1])
    else:
        messages.add_message(request, messages.ERROR, d[1])

def compress14(request, queryset):
    d = compress(request, 14)
    if d[0]:
        messages.add_message(request, messages.SUCCESS, d[1])
    else:
        messages.add_message(request, messages.ERROR, d[1])


def start_session(request):
    try:
        request.session['my_selected_objs']
    except:
        request.session['my_selected_objs'] = []


def my_list(request):
    obj_list = []
    template = loader.get_template('object/list.html')

    for x in request.session['my_selected_objs']:
        if Object.objects.filter(id=x):
            obj_list.append(Object.objects.get(id=x))

    context = {
        'request': request,
        'total': len(request.session['my_selected_objs']),
        'list': obj_list
    }
    return HttpResponse(template.render(context, request))


def my_list_action(request):
    if not request.method == 'POST':
        return redirect('/mylist/')

    if request.method == 'POST':
        action = request.POST.get('action')

        # remove selected obj from my list
        if action == 'my_list_remove_obj':
            '''
            não funciona
            request.session['x'] = []

            1   criar lista
            2   adicionar a session
            '''
            start_session(request)

            # cria lista temp
            tmp = [] # id
            for o in request.session['my_selected_objs']:
                tmp.append(int(o))

            # remove da lista não vazia
            if tmp:
                if request.POST.getlist('selected_obj'):
                    for o in request.POST.getlist('selected_obj'):
                        print(o)
                        if int(o) in tmp:
                            tmp.remove(int(o))
                            print('remove')

                    request.session['my_selected_objs'] = tmp
                    del(tmp)
                    messages.add_message(request, messages.SUCCESS, 'Removido com sucesso!')

        # limpar minha lista
        if action == 'my_list_clean':
            del request.session['my_selected_objs']
            start_session(request)
            messages.add_message(request, messages.SUCCESS, 'Lista de objectos está vazia!')

        # compactar e download
        if 'compress' in action:
            if action == 'compress3':
                compress3(request)
            if action == 'compress7':
                compress7(request)
            if action == 'compress10':
                compress10(request)
            if action == 'compress14':
                compress14(request)

        # return default
        return redirect('/mylist/')
