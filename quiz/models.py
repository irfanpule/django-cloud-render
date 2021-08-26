from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from cloudgame import utils


class Quiz(models.Model):
    title = models.CharField(_("Judul"), max_length=220)
    max_question = models.IntegerField(
        _("Maksimal Pertanyaan"), default=10,
        help_text=_("Masukan jumlah maksimal dari pertanyaan pada quiz ini.")
    )
    instruction = RichTextUploadingField(
        _("Instrukti"), help_text=_("Tuliskan instruksi yang menjelaskan tentang quiz ini.")
    )
    background_color = models.CharField(
        _("Warna Latar"), max_length=20, choices=utils.BG_COLOR, default=utils.BG_COLOR[1][0],
        help_text=_("Warna yang dipilih akan menjadi warna latar pada quiz ini.")
    )

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quiz")

    def __str__(self):
        return self.title

    @property
    def get_detail_url(self):
        url = reverse('quiz:detail', args=[self.pk])
        return url

    @property
    def get_list_url(self):
        url = reverse('quiz:list')
        return url

    @property
    def playing_url(self):
        url = reverse('quiz:playing', args=[self.pk])
        return url


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, verbose_name=_("Quiz"), blank=True)
    background_color = models.CharField(
        _("Warna Latar"), max_length=20, choices=utils.BG_COLOR, default=utils.BG_COLOR[4][0],
        help_text=_("Warna yang dipilih akan menjadi warna latar pada quiz ini.")
    )
    button_color = models.CharField(
        _("Warna Tombol"), max_length=20, choices=utils.BTN_COLOR, default=utils.BTN_COLOR[2][0],
        help_text=_("Warna yang dipilih akan menjadi warna tombol pilihan jawaban pada quiz ini.")
    )
    content = RichTextUploadingField(_("Pertanyaan"), help_text=_("Tuliskan pertanyaan disini"))

    class Meta:
        verbose_name = _("Pertanyaan")
        verbose_name_plural = _("Pertanyaan")

    def __str__(self):
        return self.content

    @property
    def get_preview_url(self):
        url = reverse('quiz:preview', args=[self.pk])
        return url


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("Pertanyaan"), on_delete=models.CASCADE)
    content = models.CharField(
        _("Konten"), max_length=220,
        help_text=_("Tuliskan jawaban yang akan muncul pada pertanyaan.")
    )
    is_correct = models.BooleanField(
        _("Jawaban Benar"), blank=False, default=False,
        help_text=_("Centang jika ini jawaban yang benar.")
    )

    class Meta:
        verbose_name = _("Jawaban")
        verbose_name_plural = _("Jawaban")

    def __str__(self):
        return self.content
