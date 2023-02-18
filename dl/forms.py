from pathlib import Path

from django import forms

from .models import UploadFile


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['serial_number', 'file', ]

    def my_form_valid(self):
        """ 投稿されたファイルのファイル名 serial_numberに変更して file_name 属性に格納する """
        instance = self.save(commit=False)
        if instance.file:
            instance.file_name = instance.serial_number + Path(instance.file.name).suffix
        instance.save()

        return instance
