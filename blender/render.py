import subprocess
import shlex
import os
import threading

from django.conf import settings
from blender.models import Project


class BlenderRender:
    log_dir = settings.RENDER_LOG_DIR
    output_dir = settings.BASE_DIR + "/output_render/frame_result"

    def __init__(self, project: Project) -> None:
        self.project = project
        self.filepath = project.file.path

    def _prepare_log_dir(self):
        """
        Create log dir if not exist
        """
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

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

    def run(self, start_frame: int, end_frame: int, option_cycles: str = "CPU", total_thread: int = 2):
        """
        to start process rendering
        :param start_frame: number of start frame
        :param end_frame: number of end frame
        :param option_cycles: option cycles rendering
        :param total_thread: number of used thread
        :return:
        """
        self._prepare_log_dir()
        self.project.state = Project.IN_PROGRESS
        self.project.save()

        args = shlex.split(
            f"blender -b {self.filepath} -o {self.output_dir} -s {start_frame} -e {end_frame} -t {total_thread} -a -- --cycles-device {option_cycles}")
        proc_render = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        t = threading.Thread(target=self._output_reader, args=(proc_render,))
        t.start()
        return t

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


class BlenderUtils:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def get_total_frames(self, script_path: str) -> int:
        """
        to get total frame from blender command extended script show_total_frame.py
        :param script_path: path file from
        :return: number of total frame
        """
        args = shlex.split(f"blender -b {self.filepath} --python {script_path}")
        output = subprocess.run(args, capture_output=True)
        output_str = output.stdout.decode("utf-8")

        for o in output_str.splitlines():
            parsing = o.split(":")
            if parsing[0].lower() == "end frame":
                return int(parsing[1])
        raise Exception("Can't get total frame. Please check your file")
