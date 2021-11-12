from django.shortcuts import get_object_or_404
from blender.models import Project
from blender.render import BlenderRender
from django.http import JsonResponse


def render_log(request, id):
    from_line = request.GET.get("from_line", 0)
    project = get_object_or_404(Project, id=id)
    br = BlenderRender(project)
    log = br.get_log(int(from_line))

    progress = get_percentage_progress(
        start_frame=request.session['start_frame'],
        end_frame=request.session['end_frame'],
        current_frame=get_current_frame(log)
    )
    return JsonResponse(data={
        "rendering": {
            "id": br.project.uuid,
            "state": br.project.state
        },
        "log": log,
        "progress": progress
    })


def get_percentage_progress(start_frame: int, end_frame: int, current_frame: int) -> float:
    total = len(range(start_frame-1, end_frame))
    return current_frame / total * 100


def get_current_frame(log: str):
    for line in log:
        line_split = line.split(" ")
        get_frame = line_split[0].split(":")
        if get_frame[0].lower() == "fra":
            return int(get_frame[1])
    return 1
