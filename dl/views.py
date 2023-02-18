import mimetypes
from pathlib import Path
from urllib import parse

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from dl.forms import UploadForm
from dl.models import UploadFile

app_name = 'dl'


class MyFormValidMixin:
    def __init__(self):
        self.request = None

    def my_form_valid(self, form):
        """ 投稿されたファイルのファイル名 serial_numberに変更して file_name 属性に格納する """
        instance = form.save(commit=False)
        if instance.file:
            instance.file_name = instance.serial_number + Path(instance.file.name).suffix
        instance.save()
        messages.success(self.request,
                         f'{instance.file.name}をアップロードしてダウンロード時のファイル名を{instance.file_name}にしました。')
        return super().form_valid(form)


class FileUploadView(MyFormValidMixin, CreateView):
    model = UploadFile
    fields = ['serial_number', 'file', ]
    template_name = 'dl/upload.html'
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'FileUploadViewを使う'
        return context

    def form_valid(self, form):
        return self.my_form_valid(form)

    def get_success_url(self):
        return self.success_url


class FileUploadViewByForm(CreateView):
    form_class = UploadForm
    model = UploadFile
    template_name = 'dl/upload.html'
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'FileUploadViewByFormを使う'
        return context

    def form_valid(self, form):
        instance = form.my_form_valid()
        messages.success(self.request,
                         f'{instance.file.name}をアップロードしてダウンロード時のファイル名を{instance.file_name}にしました。')
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
    # template_name はモデル名_list.html
    model = UploadFile
    ordering = ['-id']


class FileUpdateView(UpdateView):
    # template_name はモデル名_form.html
    model = UploadFile
    form_class = UploadForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.my_form_valid()
        return super().form_valid(form)


class FileDeleteView(DeleteView):
    # template_name はモデル名_confirm_delete.html
    model = UploadFile
    success_url = reverse_lazy('list')


def delete_func(request, pk):
    if request.method != 'POST':
        messages.warning(request, 'POSTメソッドでアクセスしてください。')
        return redirect('list')
    instance = get_object_or_404(UploadFile, pk=pk)
    instance.delete()
    messages.success(request, f'{instance.file.name}を削除しました。')
    return redirect('list')
