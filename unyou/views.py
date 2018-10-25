from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters import FilterSet, filters
from django_filters.views import FilterView
from django.db import transaction
from pure_pagination.mixins import PaginationMixin

from unyou.filters import UnyouFilter
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
from datetime import datetime, timedelta, date
from pytz import timezone, utc
from django.core.management.base import BaseCommand
from django.db import transaction
import csv
import gzip
import shutil
import os


class UnyouFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Unyou
    filterset_class = UnyouFilter
    paginate_by = 25
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


def post_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    queryset = UnyouFilter(FilterSet)

    writer = csv.writer(response)

    model = queryset.model

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
