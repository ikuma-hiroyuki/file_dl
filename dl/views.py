import mimetypes
from pathlib import Path
from urllib import parse

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from dl.forms import UploadForm
from dl.models import UploadFile

app_name = 'dl'


class FileUploadView(CreateView):
    model = UploadFile
    fields = ['serial_number', 'file', ]
    template_name = 'dl/upload.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        """ 投稿されたファイルのファイル名 serial_numberに変更して file_name 属性に格納する """
        instance = form.save(commit=False)
        instance.file_name = instance.serial_number + Path(instance.file.name).suffix
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class FileUploadViewByForm(CreateView):
    model = UploadFile
    template_name = 'dl/upload.html'
    fields = '__all__'
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'form': UploadForm(),
            'title': 'forms.pyのUploadFormを使う'
        }
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.file_name = instance.serial_number + Path(instance.file.name).suffix
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class FileDownloadView(View):
    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(UploadFile, pk=kwargs['pk'])

        # download response にするための処理
        response = HttpResponse(content_type=mimetypes.guess_type(instance.file_name))

        # ファイル名が2バイト文字のとき用の対応
        quoted_name = parse.quote(instance.file_name)
        response['Content-Disposition'] = f"attachment; filename='{quoted_name}'; filename*=UTF-8''{quoted_name}"

        return response


class FileListView(ListView):
    model = UploadFile
    # template_name はモデル名_form.html


class FileUpdateView(UpdateView):
    model = UploadFile
    fields = ['serial_number', 'file', ]
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.file_name = instance.serial_number + Path(instance.file.name).suffix
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)


class FileDeleteView(DeleteView):
    model = UploadFile
    success_url = reverse_lazy('list')
    # template_name はモデル名_confirm_delete.html
