import hou
import toolutils
import os
import hou
import shutil
import random
import datetime
import webbrowser



def go():
    # Get params
    hip = hou.expandString('$HIP')
    fps = hou.expandString('$FPS')
    normalized_path_hip = os.path.normpath(hip)
    path_components_hip = normalized_path_hip.split(os.sep)
    #print(normalized_path_hip)


    #popup ask multi input
    start_int, end_int = [1001, 1250]
    button_idx, values = hou.ui.readMultiInput(
    "Set the new frame range", ("Start Frame", "End Frame"),
    initial_contents=(str(start_int), str(end_int)),
    title="Frame Range",
    buttons=("OK", "Cancel"),
    default_choice=0, close_choice=1,)
    new_start_int = int(values[0])
    new_end_int = int(values[1])
    print (new_start_int)
    print (new_end_int)



    # gen random
    n = str(random.randint(0, 9999))
    print(n)
    randfolder = ("temp" + n)

    os.chdir(normalized_path_hip)
    os.mkdir(randfolder)

    output_path = os.path.join(normalized_path_hip, randfolder)
    print(output_path)

    filename = n + ".$F.jpg"
    flipname = os.path.join(output_path, filename)
    print(flipname)

    os.chdir(normalized_path_hip)
    flip_path = os.path.join(normalized_path_hip, "flipbook")
    if not os.path.exists(flip_path):
        os.mkdir("flipbook")
    dailies_folder = os.path.join(normalized_path_hip, "flipbook")

    # get current viewer and duplicate
    viewer = toolutils.sceneViewer()
    newviewer = viewer.clone()
    newviewer_panel = newviewer.floatingPanel()
    view = newviewer.curViewport()

    # clean up UI bars
    newviewer.setShowNetworkControls(0)
    newviewer.showOperationBar(0)
    newviewer.showDisplayOptionsBar(0)
    newviewer.showSelectionBar(0)
    newviewer_panel.setPosition([0, 0])  # position to bottom left

    # resize new viewer by cam
    # cam = viewer.curViewport().camera()

    # MANAGE FLIPBOOK SETTINGS

    # Flip Settings
    crop_mask = True
    useres = False
    #start_frame = int(hou.hscriptExpression("$FSTART"))
    #end_frame = int(hou.hscriptExpression("$FEND"))
    start_frame = new_start_int
    end_frame = new_end_int

    # Copy the viewer's current flipbook settings
    flipbook_options = newviewer.flipbookSettings().stash()

    # Change the settings however you need
    # (for example, set the frame range and output filename)
    flipbook_options.frameRange((start_frame, end_frame))
    flipbook_options.output(flipname)
    flipbook_options.cropOutMaskOverlay(crop_mask)
    flipbook_options.useResolution(useres)

    # Generate the flipbook using the modified settings
    newviewer.flipbook(newviewer.curViewport(), flipbook_options)

    # FINISH
    # close temporary panel
    newviewer.close()

    ###################ffmpeg

    burn_fps = str(fps)
    burn_text = "BCN Visuals.." + "..fps=" + burn_fps + "..start=" + str(start_frame) + "..end=" + str(
        end_frame) + "..frames=" + str(end_frame - start_frame)

    time = datetime.datetime.now()
    time = str((time.strftime("%Y.%m.%d_%H.%M.%S")))
    dailyname = time
    videoname = os.path.join(dailies_folder, dailyname)

    set = ("-start_number ", start_frame, " -framerate ", fps, " -i ", n, ".%d.jpg", " -vf ", '"',
           "pad=ceil(iw/2)*2:ceil(ih/2)*2,", "drawtext=text=", burn_text,
           ":x=(main_w)*0.02:y=(main_h)*0.98:fontsize=12:fontcolor=white", '"', " -vcodec libx264 -crf 28 -y -an ",
           videoname, ".mp4",)
    params = tuple(map(str, set))
    settings = "".join(params)
    print("ffmpeg " + settings)

    # set = ("-start_number ", start_frame, " -framerate ", fps, " -i ", n, ".%04d.jpg",
    #        ' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"', " -vcodec libx265 -crf 28 -y -an ", videoname, ".mp4",)
    # params = tuple(map(str, set))
    # settings = "".join(params)
    # print(("ffmpeg " + settings))

    os.chdir(output_path)
    os.system("ffmpeg " + settings)
    os.chdir("../")
    shutil.rmtree(output_path)

    # open flipbook folder
    webbrowser.open(flip_path)


    print("DONE FFMPEG")
    print("REMOVED JPGS")

    print("done")
