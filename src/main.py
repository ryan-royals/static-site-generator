import os
import shutil


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


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    files_from_dir("./static", "./public")


main()
