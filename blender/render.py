import subprocess
import shlex
import os
import glob

from django.conf import settings
from blender.models import Project


class BlenderRender:
    log_dir = settings.RENDER_LOG_DIR
    output_dir = settings.OUTPUT_RENDER

    def __init__(self, project: Project, start_frame: int = 0, end_frame: int = 0,
                 option_cycles: str = "CPU", total_thread: int = 2) -> None:
        self.project = project
        self.filepath = project.file.path
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.option_cycles = option_cycles
        self.total_thread = total_thread
        self.output_dir = self._generate_output_dir()

    def _generate_output_dir(self):
        output_project_dir = os.path.join(self.output_dir, self.project.slug)
        return output_project_dir + "/" + self.project.slug

    def _prepare_log_dir(self):
        """
        Create log dir if not exist
        """
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if os.path.exists(self._log_file_path()):
            os.remove(self._log_file_path())

    def _log_file_path(self) -> str:
        """
        Return absolute log file path of current project model
        :return: string path
        """
        filename = os.path.basename(self.filepath)
        name, _ = os.path.splitext(filename)
        return os.path.join(self.log_dir, name)

    def _write_log(self, line):
        """
        Write line to log file of project rendering
        :param line: string to write into file
        :return:
        """
        with open(self._log_file_path(), 'a+') as f:
            f.write(line)

    def _output_reader(self, proc):
        """
        Read process output
        :param proc: instance from subprocess
        :return:
        """
        self._write_log("Process Started\n")
        for line in iter(proc.stdout.readline, b''):
            line_str = line.decode('utf-8')
            self._write_log(line_str)

        proc.wait()
        return_code = proc.returncode
        self._write_log(f"Process exited with return code: {return_code}\n")

        if return_code == 0:
            self.project.state = Project.SUCCESS
            self.project.save()
        else:
            self.project.state = Project.FAILED
            self.project.save()

    def _remove_result_render(self):
        """
        this function is used to remove all the old renders.
        :return:
        """
        for path in glob.glob(self.output_dir + "/*"):
            try:
                os.remove(path)
            except Exception as e:
                print(e)

    def run(self):
        """
        to start process rendering
        :return:
        """
        self._prepare_log_dir()
        self._remove_result_render()
        self.project.state = Project.IN_PROGRESS
        self.project.save()

        args = shlex.split(
            f"blender -b {self.filepath} -o {self.output_dir} -s {self.start_frame} -e {self.end_frame} -t {self.total_thread} -a -- --cycles-device {self.option_cycles}")
        proc_render = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._output_reader(proc_render)

    def get_log(self, from_line=0):
        """
        Get log lines from current processing
        :param from_line: number of line to read log
        :return:
        """
        assert self.project is not None

        if os.path.exists(self._log_file_path()):
            with open(self._log_file_path(), 'r') as f:
                lines = f.readlines()

            return lines[from_line:]
        else:
            return []

    def info(self) -> dict:
        return {
           'project_id': self.project.id,
           'start_frame': self.start_frame,
           'end_frame': self.end_frame,
           'option_cycles': self.option_cycles,
           'total_thread': self.total_thread
        }
