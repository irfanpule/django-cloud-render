from celery import shared_task
from blender.render import BlenderRender
from blender.models import Project


@shared_task
def render_on_background(project_id: int, start_frame: int, end_frame: int,
                         option_cycles: str = "CPU", total_thread: int = 2):
    project = Project.objects.get(id=project_id)
    blender_render = BlenderRender(
        project=project,
        start_frame=start_frame,
        end_frame=end_frame,
        total_thread=total_thread,
        option_cycles=option_cycles
    )
    blender_render.run()
    return blender_render.info()
