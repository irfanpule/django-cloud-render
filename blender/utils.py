import subprocess
import shlex
import os

from datetime import datetime, timedelta
from django.conf import settings


def get_status_frame(start_frame: int, end_frame: int, current_frame: int) -> str:
    """
    This function to get status frame from rendering process
    :param start_frame: value int to define start frame
    :param end_frame: value int to define end frame
    :param current_frame: value int to define current frame
    :return: string status frame
    """
    frames = [*range(start_frame, end_frame + 1)]
    position = frames.index(current_frame)
    total_frame = len(frames)
    return f"Total rendered frames: {position + 1} out of {total_frame}"


def get_current_frame(log: str) -> int:
    """ Thins function to get current frame from rendering process
    :param log: string log data
    :return: number of current frame
    """
    for line in log:
        line_split = line.split(" ")
        get_frame = line_split[0].split(":")
        if get_frame[0].lower() == "fra":
            return int(get_frame[1])
    return 1


def get_percentage_progress(log: str) -> float:
    """
    This function to get percentage progress from render process
    :param log: string log data
    :return: percentage progress
    """
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


def get_total_frames(filepath: str) -> int:
    """
    to get total frame from blender command extended script show_total_frame.py
    :param filepath: filepath blender project
    :return: number of total frame
    """
    script_path = os.path.join(settings.BLENDER_SCRIPTS, "show_total_frame.py")
    args = shlex.split(f"blender -b {filepath} --python {script_path}")
    output = subprocess.run(args, capture_output=True)
    output_str = output.stdout.decode("utf-8")

    for o in output_str.splitlines():
        parsing = o.split(":")
        if parsing[0].lower() == "end frame":
            return int(parsing[1])
    raise Exception("Can't get total frame. Please check your file")
