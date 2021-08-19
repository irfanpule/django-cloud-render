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
