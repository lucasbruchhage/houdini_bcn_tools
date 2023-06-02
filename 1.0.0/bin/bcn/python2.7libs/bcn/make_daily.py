import hou
import shutil
import random
import datetime
import hou
import os
import os.path
from os import path


def go():
    # get Desktop
    desktop = hou.ui.curDesktop()
    scene = desktop.paneTabOfType(hou.paneTabType.SceneViewer)

    # gen random
    n = str(random.randint(0, 9999))
    print(n)
    rand_folder = ("temp" + n)

    # get params
    fps = int(hou.expandString('$FPS'))
    ulc = hou.expandString('$ULC')
    uid = hou.expandString('$UID')
    pid = hou.expandString('$PID')
    bcn = hou.expandString('$BCN')


    # define params
    seq_name = pid + ".$F.jpg"

    # define file path
    path_output = os.path.join(ulc, uid, pid, "daily")
    path_output_norm = os.path.normpath(path_output)
    path_base = os.path.join(ulc, uid)
    path_base_norm = os.path.normpath(path_base)
    path_new_dir = os.path.join(pid, "daily")
    path_flip_out = os.path.join(ulc, uid, pid, "daily", rand_folder, seq_name)
    path_flip_out_norm = os.path.normpath(path_flip_out)
    path_flip_out_path = os.path.join(ulc, uid, pid, "daily", rand_folder)
    path_flip_out_path_norm = os.path.normpath(path_flip_out_path)

    # folder
    if path.exists(path_output_norm):
        print ("path exists, will prev")
        # create temp folder
        os.chdir(path_output_norm)
        os.mkdir(rand_folder)

    else:
        print("path does not exist, will create it for you")
        os.chdir(path_base_norm)
        os.makedirs(path_flip_out_path_norm)
        print("created folder")

    # Flip Settings
    crop_mask = True
    use_res = False
    start_frame = int(hou.hscriptExpression("$FSTART"))
    end_frame = int(hou.hscriptExpression("$FEND"))

    # Copy the viewer's current flipbook settings
    flipbook_options = scene.flipbookSettings().stash()

    # Change the settings however you need
    # (for example, set the frame range and output filename)
    flipbook_options.frameRange((start_frame, end_frame))
    flipbook_options.output(path_flip_out_norm)
    flipbook_options.cropOutMaskOverlay(crop_mask)
    flipbook_options.useResolution(use_res)
    flipbook_options.antialias(hou.flipbookAntialias.Fast)

    # Generate the flipbook using the modified settings
    scene.flipbook(scene.curViewport(), flipbook_options)

    # ffmpeg
    time = datetime.datetime.now()
    time = str((time.strftime("%Y.%m.%d_%H.%M.%S")))
    daily_path = os.path.join(ulc, uid, pid, "daily", rand_folder, pid)
    daily_path_norm = os.path.normpath(daily_path)
    daily_name = pid + "_" + time
    video_name = os.path.join(path_output_norm, daily_name)
    font_file = os.path.join(bcn, "config", "fonts", "font.ttf")
    font_file = os.path.normpath(font_file)
    font_file = str(font_file)
    font_file = font_file.encode('unicode_escape')
    burn_fps = str(fps)
    burn_text = "BCN.." + pid + "..fps=" + burn_fps + "..start=" + str(start_frame) + "..end=" + str(end_frame) + "..frames=" + str(end_frame-start_frame)

    set = ("-start_number ", start_frame, " -framerate ", fps, " -i ", daily_path_norm, ".%04d.jpg", " -vf ", '"', "pad=ceil(iw/2)*2:ceil(ih/2)*2,", "drawtext=text=", burn_text, ":x=(main_w)*0.02:y=(main_h)*0.98:fontsize=11:fontcolor=white", '"', " -vcodec libx264 -crf 28 -y -an ", video_name, ".mp4",)
    params = tuple(map(str, set))
    settings = "".join(params)
    print ("ffmpeg " + settings)

    os.chdir(path_flip_out_path_norm)
    os.system("ffmpeg " + settings)
    os.chdir("../")
    shutil.rmtree(path_flip_out_path_norm)

    print("DONE FFMPEG")
    print("REMOVED JPGS")

    print "done"
    print(font_file)

    # burn in

