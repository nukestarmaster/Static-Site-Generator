import os
import re
import shutil


def copy_dir(source, destination):
    if not os.path.exists(source):
        raise ValueError("Source is not valid path")
    if not os.path.exists(destination):
        raise ValueError("Destination is not valid path")
    files = os.listdir(source)
    for f in files:
        origin = os.path.join(source, f)
        dest = os.path.join(destination, f)
        if os.path.isfile(origin):
            shutil.copy(origin, dest)
        if os.path.isdir(origin):
            os.mkdir(dest)
            copy_dir(origin, dest)

def copy_static():
    shutil.rmtree("public", True)
    os.mkdir("public")
    copy_dir("static", "public")

def extract_title(text):
    match = re.search("/# (.)/g")
    if match is None:
        raise ValueError("Markdown does not contain ")

