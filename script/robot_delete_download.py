# -*- coding: utf-8 -*-

'''
apagar o arquivo temporario do bucket
quando a data do campo expiry_link vencer,
for menor que o dia corrente.
'''

DEBUG = False

from datetime import datetime
import sys, os
from django.core.wsgi import get_wsgi_application

# full path to Python libray
python_bin_path = os.popen("which python").read().strip()
sys.path.append(python_bin_path)

# append paths inside of project
path = os.getcwd()
sys.path.append("..")

# import Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'archive.settings'
application = get_wsgi_application()

from object.models import Download

print("# # # Ec-Archive")
print("# Delete experied download link")
total = 0 # counter

# filter by extension
for obj in Download.objects.filter(expiry_link__lte=datetime.today()):
    print("\n+ ID : %s" % obj.id)
    print("  KEY: %s" % obj.key)
    cmd = "aws s3 rm %s" % obj.key
    os.system(cmd)

    obj.content += '\nArquivo apagado do bucket temporario pelo Crontab dia %s' % datetime.today()
    obj.content += '\n%s' % obj.key

    obj.save()
    total += 1

print("\n+Total deleted:", total)
