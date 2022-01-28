import os

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from blender.models import Project
from blender.render import BlenderRender
from blender.utils import get_percentage_progress, get_current_frame, get_status_frame, get_total_frames
from api.serializers import ProjectSerializer, RenderSerializer
from blender import tasks

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView


class CheckAuthAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": _("Your authentication is valid")})


class GetProjectsAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class UploadFileAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return self.create(request, *args, **kwargs)


class RenderAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        serializer = ProjectSerializer(project)
        data = serializer.data.copy()
        data['total_frame'] = self._get_total_frame(project)
        data['max_thread'] = os.cpu_count()
        response = {'data': data, 'message': _("Success get detail spec server")}
        return Response(response)

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        total_frame = self._get_total_frame(project)
        serializer = RenderSerializer(data=request.data, total_frame=total_frame)
        response = {}
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
            data = serializer.data
            return Response({"data": data, "message": _(f"Project {project.id} Rendered")}, status=status.HTTP_200_OK)
        else:
            response["message"] = "There's an error"
            response["errors"] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def _get_total_frame(self, project):
        total_frame = get_total_frames(filepath=project.file.path)
        return total_frame


class GetRenderLog(APIView):

    def get(self, request, id):
        from_line = request.GET.get("from_line", 0)
        project = get_object_or_404(Project, id=id)
        br = BlenderRender(project)
        log = br.get_log(int(from_line))

        progress = get_percentage_progress(log)
        data = {
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
        }
        return Response({
            "data": data,
            "message": _("succes get progress data")
        })
