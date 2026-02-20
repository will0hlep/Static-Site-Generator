import os
import shutil
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode


def main():
    static_to_public()
    generate_page('content/index.md', 'template.html', 'public/index.html')
    return None


def static_to_public():
    shutil.rmtree('public')
        
    def static_to_public_copy_routine(path):
        static_path = os.path.join('static', path)
        public_path = os.path.join('public', path)
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


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_string)
    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path, "w") as f:
        f.write(template)
        f.close()
    return None

main()