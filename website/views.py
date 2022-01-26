from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from blender.forms import FormUpload, PreRender
from blender.models import Project
from blender import tasks
from blender.utils import get_total_frames


def _get_project(request):
    project = Project.objects.filter(id=request.session.get("project_uuid", None)).first()
    if not project:
        messages.warning(request, _('You have to upload your blender project first'))
        return redirect('website:index')
    return project


@login_required
def index(request):
    form = FormUpload(request.POST or None, files=request.FILES)
    if form.is_valid():
        project = form.save()
        request.session["project_uuid"] = project.uuid
        return redirect('website:pre_render')

    context = {
        'title': _('Home'),
        'form': form,
        'title_submit': _('Upload')
    }
    return render(request, 'website/index.html', context)


def pre_render(request):
    project = _get_project(request)
    total_frame = get_total_frames(filepath=project.file.path)

    form = PreRender(request.POST or None, initial={'start_frame': 1, 'end_frame': total_frame})
    if form.is_valid():
        request.session['start_frame'] = form.cleaned_data['start_frame']
        request.session['end_frame'] = form.cleaned_data['end_frame']
        tasks.render_on_background.delay(
            project_id=project.id,
            start_frame=form.cleaned_data['start_frame'],
            end_frame=form.cleaned_data['end_frame'],
            total_thread=form.cleaned_data['total_thread'],
            option_cycles=form.cleaned_data['option_cycles']
        )
        return redirect("website:rendering")

    context = {
        'title': _('Pre Render'),
        'total_frame': total_frame,
        'project': project,
        'title_submit': _('Process'),
        'form': form,
    }
    return render(request, 'website/pre-render.html', context)


def process_render(request):
    project = _get_project(request)
    context = {
        'title': _('Rendering'),
        'project': project,
    }
    return render(request, 'website/rendering.html', context)


def result_render(request):
    project = _get_project(request)
    context = {
        'title': _("Result"),
        'project': project,
    }
    return render(request, "website/result.html", context)


def download_result(request):
    project = _get_project(request)
    zip_buffer = project.export_result_to_zip_bytes_io()
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % f'{project.slug}.zip'
    return response
