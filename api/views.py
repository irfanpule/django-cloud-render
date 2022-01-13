import os

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from blender.models import Project
from blender.render import BlenderRender
from blender.utils import get_percentage_progress, get_current_frame, get_status_frame
from api.serializers import ProjectSerializer, RenderSerializer
from blender.render import BlenderUtils
from blender import tasks

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


def _get_project(request):
    project = Project.objects.filter(id=request.session.get("project_uuid", None)).first()
    if not project:
        return Response({
            "message": _('You have to upload your blender project first')
        }, status=status.HTTP_400_BAD_REQUEST)
    return project


class GetSessionAPIView(APIView):

    def get(self, request):
        return Response({
            "message": "success",
            "project_uuid": request.session.get("project_uuid")
        })


class UploadFileAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            data = serializer.data.copy()
            data["project_uuid"] = project.uuid
            request.session["project_uuid"] = project.uuid
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RenderAPIView(APIView):

    def get(self, request):
        project = _get_project(request)
        serializer = ProjectSerializer(project)
        data = serializer.data.copy()
        data['total_frame'] = self._get_total_frame(project)
        data['max_thread'] = os.cpu_count()
        return Response(data)

    def post(self, request):
        project = _get_project(request)
        total_frame = self._get_total_frame(project)
        serializer = RenderSerializer(data=request.data, total_frame=total_frame)
        if serializer.is_valid():
            request.session['start_frame'] = serializer.validated_data['start_frame']
            request.session['end_frame'] = serializer.validated_data['end_frame']

            tasks.render_on_background.delay(
                project_id=project.id,
                start_frame=serializer.validated_data['start_frame'],
                end_frame=serializer.validated_data['end_frame'],
                total_thread=serializer.validated_data['total_thread'],
                option_cycles=serializer.validated_data['option_cycles']
            )
            return Response({"message": f"Project {project.id} Rendered"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_total_frame(self, project):
        bu = BlenderUtils(filepath=project.file.path)
        script_path = os.path.join(settings.BLENDER_SCRIPTS, "show_total_frame.py")
        total_frame = bu.get_total_frames(script_path)
        return total_frame


class GetRenderLog(APIView):

    def get(self, request, id):
        from_line = request.GET.get("from_line", 0)
        project = get_object_or_404(Project, id=id)
        br = BlenderRender(project)
        log = br.get_log(int(from_line))

        progress = get_percentage_progress(log)
        return Response({
            "rendering": {
                "id": br.project.uuid,
                "state": br.project.state
            },
            "log": log,
            "progress": progress,
            "status_frame": get_status_frame(
                request.session["start_frame"],
                request.session["end_frame"],
                get_current_frame(log)
            )
        })
