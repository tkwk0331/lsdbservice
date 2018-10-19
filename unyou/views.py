from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters import FilterSet, filters
from django_filters.views import FilterView

from pure_pagination.mixins import PaginationMixin
from .models import Unyou
from .filters import UnyouFilter, MyOrderingFilter
from .forms import UnyouForm
import csv
import gzip
import shutil
import os
import csv
import io
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic



class UnyouFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Unyou
    filterset_class = UnyouFilter
    paginate_by =25
    object = Unyou
 # クエリ未指定の時に全件検索を行うために以下のオプションを指定（django-filter2.0以降）
strict = False

# pure_pagination用設定


# 検索条件をセッションに保存する or 呼び出す
def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


class PostImport(LoginRequiredMixin, PaginationMixin, FilterView):
    success_url = reverse_lazy('index')
    filterset_class = UnyouFilter

def post_export(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。

    model = Unyou
    filterset_class = UnyouFilter

    queryset = Unyou.objects.all()

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
    writer = csv.writer(response)

    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
        writer.writerow(headers)


    for obj in queryset:
        row = []
        for field in headers:
            val = getattr(obj, field)
        if callable(val):
            val = val()
            row.append(val)
            writer.writerow(row)

        return response
    '''
    model = Unyou
    filterset_class = UnyouFilter
    object = Unyou

    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def handle(self, *args, **options):

        filename = "結果.csv"

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
        '''



# 詳細画面
class UnyouDetailView(LoginRequiredMixin, DetailView):
        model = Unyou

# 登録画面
class UnyouCreateView(LoginRequiredMixin, CreateView):
        model = Unyou
        form_class = UnyouForm
        success_url = reverse_lazy('index')

# 更新画面
class UnyouUpdateView(LoginRequiredMixin, UpdateView):
        model = Unyou
        form_class = UnyouForm
        success_url = reverse_lazy('index')
# 削除画面
class UnyouDeleteView(LoginRequiredMixin, DeleteView):
        model = Unyou
        success_url = reverse_lazy('index')
