import os
import uuid
import glob
import zipfile

from io import BytesIO
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User


class Project(models.Model):
    PREPARE = "prepare"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"

    RENDER_STATE = (
        (PREPARE, _("Prepare")),
        (IN_PROGRESS, _("In Progress")),
        (SUCCESS, _("Success")),
        (FAILED, _("Failed")),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(_("Project Name"), max_length=255)
    file = models.FileField(_("Blender File"), upload_to="uploads/")
    user_name = models.CharField(_("Your Name"), max_length=255, blank=True, null=True, help_text=_("optional"))
    state = models.CharField(_("Render State"), choices=RENDER_STATE, max_length=255, default=PREPARE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def uuid(self) -> str:
        return str(self.id)

    @property
    def slug(self) -> str:
        return slugify(self.name)

    def get_result_render(self, use_media_host=True) -> [str]:
        output_render = os.path.join(settings.OUTPUT_RENDER, self.slug)
        all_file = glob.glob(output_render + "/*")
        if use_media_host:
            realpath = []
            for file in all_file:
                realpath.append(settings.MEDIA_HOST + os.path.relpath(file))
            return realpath
        return all_file

    def export_result_to_zip_bytes_io(self) -> BytesIO:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip:
            for path in self.get_result_render(use_media_host=False):
                filename = os.path.basename(path)
                zip.write(path, filename)
        return zip_buffer
