import os
import sys
import shutil
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from pathlib import Path


def main(basepath):
    static_to_public()
    generate_pages_recursive('content', 'template.html', 'docs', basepath)
    return None


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        contnet_path = os.path.join(dir_path_content, file)
        public_path = Path(os.path.join(dest_dir_path, file))
        if os.path.isfile(contnet_path):
            generate_page(contnet_path, template_path, public_path.with_suffix('.html'), basepath)
        else:
            generate_pages_recursive(contnet_path, template_path, public_path, basepath)
    return None


def static_to_public():
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs')
        
    def static_to_public_copy_routine(path):
        static_path = os.path.join('static', path)
        public_path = os.path.join('docs', path)
        for file in os.listdir(static_path):
            passed_file_path = os.path.join(path, file)
            static_file_path = os.path.join(static_path, file)
            public_file_path = os.path.join(public_path, file)
            directory = os.path.dirname(public_file_path)
            if not os.path.exists(directory):
                os.mkdir(directory)
            if os.path.isfile(static_file_path):
                shutil.copy(static_file_path, public_file_path)
            else:
                static_to_public_copy_routine(passed_file_path)
        return None

    static_to_public_copy_routine('')
    return None


def extract_title(markdown):
    if markdown.startswith('#'):
        return markdown.split('\n')[0].strip('#').strip()
    raise Exception('no header')


def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    print(template)
    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path, "w") as f:
        f.write(template)
        f.close()
    return None


if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = '/'

main(basepath)