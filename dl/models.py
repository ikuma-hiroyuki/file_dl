from django.db import models


class UploadFile(models.Model):
    file = models.FileField(null=True, blank=True, verbose_name='ダウンロード時に使うファイル名', upload_to='images')
    file_name = models.CharField(max_length=100, verbose_name='ダウンロード時に使うファイル名')
    serial_number = models.CharField(max_length=100, verbose_name='製造番号', blank=False, null=False, unique=True,
                                     default='')

    def __str__(self):
        return self.file_name
