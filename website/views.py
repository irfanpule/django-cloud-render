from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from blender.forms import FormUpload, PreRender
from blender.models import Project
from blender import tasks
from blender.utils import get_total_frames


@login_required
def index(request):
    context = {
        'title': _('Your Project'),
        'projects': Project.objects.filter(user=request.user)
    }
    return render(request, 'website/list-project.html', context)


@login_required
def add_project(request):
    form = FormUpload(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        return redirect('website:index')

    context = {
        'title': _('Add Project'),
        'form': form,
        'title_submit': _('Upload')
    }
    return render(request, 'website/index.html', context)


@login_required
def pre_render(request, id):
    project = get_object_or_404(Project, id=id)
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
        return redirect("website:rendering", project.uuid)

    context = {
        'title': _('Pre Render'),
        'total_frame': total_frame,
        'project': project,
        'title_submit': _('Process'),
        'form': form,
    }
    return render(request, 'website/pre-render.html', context)


@login_required
def process_render(request, id):
    project = get_object_or_404(Project, id=id)
    context = {
        'title': _('Rendering'),
        'project': project,
    }
    return render(request, 'website/rendering.html', context)


@login_required
def result_render(request, id):
    project = get_object_or_404(Project, id=id)
    context = {
        'title': _("Result"),
        'project': project,
    }
    return render(request, "website/result.html", context)


@login_required
def download_result(request, id):
    project = get_object_or_404(Project, id=id)
    zip_buffer = project.export_result_to_zip_bytes_io()
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % f'{project.slug}.zip'
    return response
