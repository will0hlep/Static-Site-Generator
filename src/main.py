import os
import shutil
from textnode import TextNode, TextType

def main():
    static_to_public()


def static_to_public():
    for file in os.listdir('public'):
        shutil.rmtree(os.path.join('public', file))
    static_to_public_copy_routine('')


def static_to_public_copy_routine(path):
    static_path = os.path.join('static', path)
    public_path = os.path.join('public', path)
    for file in os.listdir(static_path):
        passed_file_path = os.path.join(path, file)
        static_file_path = os.path.join(static_path, file)
        public_file_path = os.path.join(public_path, file)
        if not os.path.exists(public_file_path):
            os.mkdir(public_file_path)
        if os.path.isfile(static_file_path):
            shutil.copy(static_file_path, public_file_path)
        else:
            static_to_public_copy_routine(passed_file_path)

main()