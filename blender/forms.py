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
        (1, _("One")),
        (2, _("Two")),
        (3, _("Three")),
        (4, _("Four"))
    )
    total_thread = forms.ChoiceField(label=_("Total Thread"), choices=THREAD_CHOICES, initial=2)
    OPTION_CHOICES = (
        ("CPU", "CPU"),
        ("CUDA+CPU", "CUDA+CPU"),
    )
    option_cycles = forms.ChoiceField(label=_("Option Cycles"), choices=OPTION_CHOICES)
