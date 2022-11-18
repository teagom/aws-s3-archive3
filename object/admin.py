# -*- coding: utf-8 -*-

from django.contrib.admin import site
from django.contrib import admin, messages
from django.utils.html import format_html

from object.views import start_session
from object.models import Object, Download


class ObjectAdmin(admin.ModelAdmin):
    class Media:
        css = {'all':('/media/bootstrap.min.css',)}
        js = ('/media/jquery-3.6.0.min.js','/media/bootstrap.min.js','/media/object_admin_modal.js')

    # mostra minha lista de obj
    def my_list_show(self, request, queryset):
        start_session(request)
        if len(request.session['my_selected_objs']) > 0:
            messages.add_message(request, messages.SUCCESS, 'Minha lista de objecto!')
        else:
            messages.add_message(request, messages.WARNING, 'A lista de objeto está vazia!')
    my_list_show.short_description = 'Minha lista - mostrar objecto selecionado'


    # add na minha lista de obj
    def my_list_add_obj(modeladmin, request, queryset):
        start_session(request)

        # guarda o que ja existe
        tmp = []
        for o in request.session['my_selected_objs']:
            tmp.append(o)

        # add novo
        for o in queryset:
            if not o.id in tmp:
                tmp.append(o.id)

        # nova lista
        request.session['my_selected_objs'] = tmp

        messages.add_message(request, messages.SUCCESS, 'Adicionado com sucesso!')
        return True
    my_list_add_obj.short_description = 'Minha lista - Adicionar objecto selecionado'


    def changelist_view(self, request, extra_context=None):
        start_session(request)
        if len(request.session['my_selected_objs']) > 0:
            link = format_html('<a target="_myObjectList" href="/mylist/">Objectos selecionados</a>')
            messages.add_message(request, messages.SUCCESS, link)
        else:
            messages.add_message(request, messages.ERROR, 'Nenhum objecto na sua lista')

        return super(ObjectAdmin, self).changelist_view(request, extra_context)


    def compress_content_list(self):
        '''
        display content of a compress file, zip or rar
        without a click to next page
        '''
        if self.key_extension in ['zip','rar']:
            return format_html('<button id="%s" type="button" class="btn btn-sm btn-primary">show</button>' % self.id)
        else:
            return 'None'
    compress_content_list.short_description = u'Content'

    search_fields = ['key','compress_content']
    list_filter = ['storageclass','bucket__name_short','key_level']
    list_display = ('bucket','key','key_extension',compress_content_list,'key_level','size_easy','etag','id','storageclass')
    actions = [my_list_add_obj]

    # avoid delete
    # avoid add
    # avoid change
    def has_delete_permission(self, request, obj=None):
        return False
    site.disable_action('delete_selected')

admin.site.register(Object, ObjectAdmin)


class DownloadAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_display = ('url','date_join','user')
    list_filter = ['user','date_join']
    readonly_fields = ['id','url','date_join','user','content','expiry_link','counter','key']
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Download, DownloadAdmin)
