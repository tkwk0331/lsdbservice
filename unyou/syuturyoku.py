from pytz import timezone, utc
from django.core.management.base import BaseCommand
import csv
import gzip
import shutil
import os
from .models import Unyou
from .filters import UnyouFilter
from .forms import UnyouForm

class Command(BaseCommand):
    model = Unyou
    filterset_class = UnyouFilter
    object = Unyou

class PostImport(generic.FormView):
        success_url = reverse_lazy('index')


    def get(self, request, **kwargs):
    if request.GET:
        request.session['query'] = request.GET
    else:
        request.GET = request.GET.copy()
        if 'query' in request.session.keys():
            for key in request.session['query'].keys():
                request.GET[key] = request.session['query'][key]

    return super().get(request, **kwargs)

def post_export(request):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="posts.csv"'
        # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。

        queryset = UnyouFilter.objects

        model = queryset.model
        writer = csv.writer(response)

        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        writer.writerow(headers)

        ## 取得したレコードを書き込む
        for obj in queryset:
            row = []
            for field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
            writer.writerow(row)

def handle(self, *args, **options):

        filename ="結果.csv"

        model = Unyou
        writer = csv.writer(open(filename, 'w'))

        ## csvのヘッダー部の書き込み
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        writer.writerow(headers)

        ## 取得したレコードを書き込む
        for obj in Unyou:
            row = []
            for field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
            writer.writerow(row)

        # csvをgzipで圧縮
        with open(filename, 'rb') as gzip_in:
            with gzip.open(filename + ".gz", 'wb') as gzip_out:
                shutil.copyfileobj(gzip_in, gzip_out)

        os.remove(filename)

        def get(self, request, **kwargs):
            if request.GET:
                request.session['query'] = request.GET
            else:
                request.GET = request.GET.copy()
                if 'query' in request.session.keys():
                    for key in request.session['query'].keys():
                        request.GET[key] = request.session['query'][key]

            return super().get(request, **kwargs)

        model = queryset.model
        writer = csv.writer(open(filename, 'w'))

        ## csvのヘッダー部の書き込み
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        writer.writerow(headers)

        ## 取得したレコードを書き込む
        for obj in queryset:
            row = []
            for field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
            writer.writerow(row)