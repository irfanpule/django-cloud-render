from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from cloudgame import utils


class MissingObject(models.Model):
    title = models.CharField(_("Judul"), max_length=220)
    instruction = RichTextUploadingField(
        _("Instrukti"), help_text=_("Tuliskan instruksi yang menjelaskan tentang quiz ini.")
    )
    background_color = models.CharField(
        _("Warna Latar"), max_length=20, choices=utils.BG_COLOR, default=utils.BG_COLOR[2][0],
        help_text=_("Warna yang dipilih akan menjadi warna latar pada quiz ini.")
    )

    class Meta:
        verbose_name = _("Pencarian Gambar")
        verbose_name_plural = _("Pencarian Gambar")

    def __str__(self):
        return self.title

    @property
    def get_detail_url(self):
        url = reverse('missing_object:detail', args=[self.pk])
        return url

    @property
    def get_list_url(self):
        url = reverse('missing_object:list')
        return url

    @property
    def playing_url(self):
        url = reverse('missing_object:playing', args=[self.pk])
        return url


class ImageObject(models.Model):
    missing_object = models.ForeignKey(
        MissingObject, verbose_name=_("Mencari Obyek"),
        related_name='imageobjects', on_delete=models.CASCADE
    )
    name = models.CharField(
        _("Nama"), max_length=220,
        help_text=_("Tuliskan nama dari obyek gambar yang diunggah.")
    )
    picture = models.ImageField(upload_to=utils.custom_upload_path('pictures'))

    class Meta:
        verbose_name = _("Obyek Gambar")
        verbose_name_plural = _("Obyek Gambar")

    def __str__(self):
        return self.name
