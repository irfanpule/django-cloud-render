import os

from django.utils.translation import ugettext_lazy as _

from blender.models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'file', 'user']

    def create(self, validated_data):
        project = Project.objects.filter(name=validated_data["name"]).first()
        if project:
            project.name = validated_data['name']
            project.file = validated_data['file']
            project.save()
            return project
        else:
            return super().create(validated_data)


class RenderSerializer(serializers.Serializer):
    start_frame = serializers.IntegerField()
    end_frame = serializers.IntegerField()
    total_thread = serializers.IntegerField(initial=2)
    option_cycles = serializers.CharField()

    def __init__(self, total_frame, *args, **kwargs):
        self.total_frame = total_frame
        super().__init__(*args, **kwargs)

    def validate_total_thread(self, value):
        cpu_count = os.cpu_count()
        if value > cpu_count:
            raise serializers.ValidationError(_(f"Maximum thread on your CPU is only {cpu_count}"))
        return value

    def validate_option_cycles(self, value):
        if value not in ['CUDA+CPU', 'CPU']:
            raise serializers.ValidationError(_("Choices from option cycles is `CPU` or `CPU+CUDA`"))
        return value

    def validate_start_frame(self, value):
        if value > self.total_frame:
            raise serializers.ValidationError(_(f"start_frame cannot be greater than {self.total_frame}"))
        return value

    def validate_end_frame(self, value):
        if value > self.total_frame:
            raise serializers.ValidationError(_(f"end_frame cannot be greater than {self.total_frame}"))
        return value
