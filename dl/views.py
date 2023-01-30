import mimetypes
from urllib import parse

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView

from dl.models import UploadFile


class FileUploadView(CreateView):
    model = UploadFile
    fields = ['file', ]
    template_name = 'dl/upload.html'

    def form_valid(self, form):
        """ 投稿されたファイルのファイル名を取得して file_name 属性に格納する """
        instance = form.save(commit=False)
        instance.file_name = instance.file.name
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class FileDownloadView(View):
    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(UploadFile, pk=kwargs['pk'])

        # download response にするための処理
        response = HttpResponse(content_type=mimetypes.guess_type(instance.file_name))

        # ファイル名が2バイト文字のとき用の対応
        quoted_name = parse.quote(instance.file_name)
        response['Content-Disposition'] = f"attachment; filename='{quoted_name}'; filename*=UTF-8''{quoted_name}"

        return response
