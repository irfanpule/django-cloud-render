import os.path
import uuid
import glob
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.conf import settings


class Project(models.Model):
    PREPARE = "prepare"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"

    RENDER_STATE = (
        (PREPARE, _("Prepare")),
        (SUCCESS, _("Success")),
        (FAILED, _("Failed")),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(_("Project Name"), max_length=255)
    file = models.FileField(_("Blender File"), upload_to="uploads/")
    user_name = models.CharField(_("Your Name"), max_length=255, blank=True, null=True, help_text=_("optional"))
    state = models.CharField(_("Render State"), choices=RENDER_STATE, max_length=255, default=PREPARE)

    def __str__(self):
        return str(self.id)

    @property
    def uuid(self):
        return str(self.id)

    @property
    def slug(self):
        return slugify(self.name)

    def get_result_render(self):
        output_render = os.path.join(settings.OUTPUT_RENDER, self.slug)
        realpath = []
        for file in glob.glob(output_render + "/*"):
            realpath.append(settings.MEDIA_HOST + os.path.relpath(file))
        return realpath


class RenderResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return str(self.id) + self.project.name
