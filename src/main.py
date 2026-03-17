import os
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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)

    page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    files_from_dir("./static", "./public")

    generate_page("content/index.md", "src/template.html", "public/index.html")


main()
