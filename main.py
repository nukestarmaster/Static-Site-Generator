import os
import re
import shutil
from src.textnode import markdown_to_html_node


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
    match = re.findall("^# (.*)", text, re.MULTILINE)
    print(match)
    if match == []:
        raise ValueError("Markdown does not contain title")
    return match[0]

def generate_page(from_path, template_path, to_path):
    print(f"Genertating page form {from_path} to {to_path} using {template_path}")
    file = open(from_path).read()
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    html =  markdown_to_html_node(file).to_html()
    title = extract_title(file)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    to_dir = os.path.dirname(from_path)
    os.makedirs(to_dir, exist_ok= True)
    newfile = open(to_path, "w")
    newfile.write(page)
    newfile.close()

def generate_page_recursive(from_path, template_path, to_path):
    dirs = os.listdir(from_path)
    for d in dirs:
        origin = os.path.join(from_path, d)
        dest = os.path.join(to_path, d)
        if os.path.isfile(origin):
            generate_page(origin, template_path, dest.split(".")[0]+".html")
        else:
            os.makedirs(dest, exist_ok = True)
            generate_page_recursive(origin, template_path, dest)

def main():
    copy_static()
    generate_page_recursive("content", "template.html", "public")

main()