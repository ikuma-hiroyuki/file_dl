# 変更点



## 2023/02/06

- migrations
  - UploadFile モデルにserial_number フィールドを追加
  - UploadFile モデルのserial_number フィールドのデフォルト値を''に変更
- admin.py にUploadFile モデルを追加
- views.py の変更
  - `app_name = 'dl'` の追加
  - fields にserial_numberを追加
  - FileUploadView クラス
    - `success_url = reverse_lazy('list')` の設定と`get_success_url` メソッドの変更
    - docstring の変更
    - instance.file_name をserial_number + 拡張子に変更
  - FileListView クラスの追加
- urls.py に`list/` を追加
- uploadfile_form.html を追加



## 2022/02/07

- migration
  - UploadFile モデルのupload_to を削除
- views.py の変更
  - UpdateView, DeleteView と対応するhtml ファイルの追加
  - FileUploadViewByForm 追加
  - FileUpdateView でfile_name変更処理の追加
- settings.py の変更
  - MEDIA_ROOT, MEDIA_URL の設定
- urls.pyの変更
  - urlpatterns に`+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` を追加
  - urlpatterns に`upload/` を追加しuploadfile_list.htmlも修正
- forms.py の追加
- settings.py の変更
  - INSTALLED_APPS にdjango_cleanup.apps.CleanupConfig を追加
  - LANGUAGE_CODE, TIMEZONE の変更