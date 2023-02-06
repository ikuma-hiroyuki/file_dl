from django.db import models


class UploadFile(models.Model):
    file = models.FileField(upload_to='dl/upload_files/')
    file_name = models.CharField(max_length=100, verbose_name='ダウンロード時に使うファイル名')
    serial_number = models.CharField(max_length=100, verbose_name='製造番号', blank=False, null=False, unique=True,
                                     default='a')

    def __str__(self):
        return self.file_name
