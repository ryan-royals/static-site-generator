import os
import sys
import shutil

from convert import markdown_to_html_node
from extract import extract_title


def files_from_dir(src, dest):
    print(f"working on dir {src}")
    files = os.listdir(src)
    for file in files:
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            print(f"copying {file_path}")
            shutil.copy(file_path, dest)
        else:
            next_dir = os.path.join(src, file)
            next_dest = os.path.join(dest, file)
            print(f"making dir {next_dest}")
            os.mkdir(next_dest)
            files_from_dir(next_dir, next_dest)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)

    page = template_content.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_node.to_html())
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"working on dir {dir_path_content}")
    files = os.listdir(dir_path_content)
    for file in files:
        file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, os.path.join(dest_dir_path, file.replace(".md", ".html")), basepath)
        else:
            next_dir = os.path.join(dir_path_content, file)
            next_dest = os.path.join(dest_dir_path, file)
            print(f"making dir {next_dest}")
            generate_pages_recursively(next_dir, template_path, next_dest, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"basepath = {basepath}")
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    os.mkdir("./docs")
    files_from_dir("./static", "./docs")

    generate_pages_recursively("content", "src/template.html", "docs", basepath)


main()
