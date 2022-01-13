import os

from django import forms
from django.utils.translation import ugettext_lazy as _
from blender.models import Project


class FormUpload(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('state',)


class PreRender(forms.Form):
    start_frame = forms.IntegerField(label=_("Start Frame"))
    end_frame = forms.IntegerField(label=_("End Frame"))
    THREAD_CHOICES = (
        (1, 1),
        (2, 2)
    )
    total_thread = forms.ChoiceField(label=_("Total Thread"), choices=THREAD_CHOICES, initial=2)
    OPTION_CHOICES = (
        ("CPU", "CPU"),
        ("CUDA+CPU", "CUDA+CPU"),
    )
    option_cycles = forms.ChoiceField(label=_("Option Cycles"), choices=OPTION_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_choices = []
        for i in range(1, os.cpu_count() + 1):
            new_choices.append([i, i])

        self.fields['total_thread'].help_text = f"Maximun thread your CPU is {os.cpu_count()}"
        self.fields['total_thread'].choices = new_choices

    def clean_start_frame(self):
        if self.cleaned_data['start_frame'] > self.initial['end_frame']:
            raise forms.ValidationError(_(f"Start frame cannot be greater than {self.initial['end_frame']}"))
        return self.cleaned_data['start_frame']

    def clean_end_frame(self):
        if self.cleaned_data['end_frame'] > self.initial['end_frame']:
            raise forms.ValidationError(_(f"Start frame cannot be greater than {self.initial['end_frame']}"))
        return self.cleaned_data['end_frame']
