import bpy


def get_total_frame():
    """
    This method to get total frame from blender file.
    This method/file must be exec use blender command because `bpy` in env blender
    How to exec it?
    `blender -b <path file> --python show_total_frame.py`
    """
    scene = bpy.context.scene
    print("End Frame: %d" % scene.frame_end)


get_total_frame()
