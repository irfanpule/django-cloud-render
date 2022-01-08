from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from blender.models import Project
from blender.render import BlenderRender
from django.http import JsonResponse


def render_log(request, id):
    from_line = request.GET.get("from_line", 0)
    project = get_object_or_404(Project, id=id)
    br = BlenderRender(project)
    log = br.get_log(int(from_line))

    progress = get_percentage_progress_v2(log)
    return JsonResponse(data={
        "rendering": {
            "id": br.project.uuid,
            "state": br.project.state
        },
        "log": log,
        "progress": progress,
    })


def get_percentage_progress(start_frame: int, end_frame: int, current_frame: int) -> float:
    total = len(range(start_frame - 1, end_frame))
    return current_frame / total * 100


def get_current_frame(log: str):
    for line in log:
        line_split = line.split(" ")
        get_frame = line_split[0].split(":")
        if get_frame[0].lower() == "fra":
            return int(get_frame[1])
    return 1


def get_percentage_progress_v2(log: str) -> float:
    for line in log:
        try:
            line_split = line.split("|")
            time = line_split[1].strip()
            remaining = line_split[2].strip()
            if time.lower().find("time") != -1 and remaining.lower().find("remaining") != -1:
                time_clean = time.rsplit("Time:")[-1]
                remaining_clean = remaining.rsplit("Remaining:")[-1]
                time_obj = datetime.strptime(time_clean.strip(), "%M:%S.%f")
                remaining_obj = datetime.strptime(remaining_clean.strip(), "%M:%S.%f")
                total_time = remaining_obj + timedelta(hours=time_obj.hour,
                                                       minutes=time_obj.minute, seconds=time_obj.second)
                total_seconds = timedelta(hours=total_time.hour, minutes=total_time.minute,
                                          seconds=total_time.second).total_seconds()
                time_seconds = timedelta(hours=time_obj.hour, minutes=time_obj.minute,
                                         seconds=time_obj.second).total_seconds()
                return round(time_seconds / total_seconds * 100, 2)
        except Exception as e:
            print(e)
            return 0.0
