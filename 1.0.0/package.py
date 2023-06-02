name = "houdini_bcn_tools"

version = '1.0.0'

requires = ['houdini']

def commands():

    env.HOUDINI_PATH.append("{root}/bin")
    env.HOUDINI_PATH.append("{root}/bin/scripts")
    env.PYTHONPATH.append("{root}/bin/scripts")
    env.HOUDINI_PACKAGE_DIR.append("{root}/bin")

