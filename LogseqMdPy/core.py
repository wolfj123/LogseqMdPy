import os
import pypandoc
import re

from LogseqMdPy.utils import *
from LogseqMdPy.graph import *
from .models import LogseqPage, LogseqBlock

class LogseqMdPy:
    def __init__(self, logseq_directory):
        self.logseq_dir = logseq_directory

    def get_logseq_dir(self):
        return self.logseq_dir

    def get_page_by_name(self, name):
        all_pages = self.get_all_pages()
        for page in all_pages:
            if page.get_page_name() == name:
                return page
        return None

    def get_all_files(self, pages = True, journals = True):
        """
        Gets a list of all markdown files from the "pages" and/or "journals" folders.

        Args:
            pages (bool): Whether to include files from the "pages" directory.
            journals (bool): Whether to include files from the "journals" directory.

        Returns:
            List[str]: A list of absolute file paths of markdown files found.
        """

        page_files = []
        folders = []

        if pages:
            # pages_path = os.path.join(os.getcwd(),  "pages")
            pages_path = os.path.join(self.get_logseq_dir(),  "pages")
            folders.append(pages_path)
        if journals:
            # journals_path = os.path.join(os.getcwd(), "journals")
            journals_path = os.path.join(self.get_logseq_dir(), "journals")
            folders.append(journals_path)

        for folder in folders:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    
                    # Check if it's a file (not a directory)
                    if os.path.isfile(file_path):
                        base, extension = os.path.splitext(file_path)
                        if extension.lower() == ".md":
                            page_files.append(file_path)
        
        return page_files

    def get_all_pages(self, pages = True, journals = True):
        all_pages = []
        for file in self.get_all_files(pages = pages, journals = journals):
            all_pages.append(LogseqPage(file))
        return all_pages

    def get_all_blocks_with_refs(self, refs, include_inherited = True):
        result = []
        all_pages = self.get_all_pages()
        for page in all_pages:
            result.extend(page.get_all_blocks_with_refs(refs, include_inherited))
        return result

    def reset_all_cards_of_page(self, page_name):
        blocks = self.get_all_blocks_with_refs(["card", page_name])
        for b in blocks:
            b.delete_properties(get_card_props())
            p = b.get_page()
            p.write_to_file()

    def disable_all_cards_of_page(self, page_name):
        blocks = self.get_all_blocks_with_refs(["card", page_name])
        for b in blocks:
            orig_text = b.get_text()
            if "#card" in orig_text and "#card-off" not in orig_text:
                new_text = orig_text.replace("#card", "#card-off")
                b.set_text(new_text)
            b.delete_properties(get_card_props())
            p = b.get_page()
            p.write_to_file()

    # Expose utility functions
    def get_reference_pattern(self):
        return get_reference_pattern()

    def get_tag_pattern(self):
        return get_tag_pattern()

    def name_to_filename(self, name):
        return name_to_filename(name)

    def filename_to_name(self, filename):
        return filename_to_name(filename)

    def count_leading_tabs(self, text):
        return count_leading_tabs(text)

    def sanitize_filename(self, filename):
        return sanitize_filename(filename)

    def h(self, text, level):
        return h(text, level)

    def bold(self, text):
        return bold(text)

    def italic(self, text):
        return italic(text)

    def tag(self, text):
        return tag(text)

    def is_page_ref(self, text):
        return is_page_ref(text)

    def page_ref(self, text):
        return page_ref(text)

    # Expose graph functions
    def create_networkx_directed_graph_from_pages(self, pages):
        return create_networkx_directed_graph_from_pages(pages)

    def create_gephi_file_from_pages(self, pages, output_file):
        return create_gephi_file_from_pages(pages, output_file)
    
    # Expose constructors for LogseqPage and LogseqBlock
    def LogseqPage(self, file_path):
        return LogseqPage(file_path)

    def LogseqBlock(self):
        return LogseqBlock()
    
    def export_to_html(self, page, output_dir, css_file = None):
        # Change the current working directory to the directory of the page's file
        # page_dir = os.path.dirname(page.get_file())
        # os.chdir(page_dir)
        tmp_filename = "tmpFileForExport.md"

        page_copy = page.copy()
        page_copy.delete_blocks_with_property("export","false")
        page_copy.remove_all_properties()
        page_copy.remove_all_references()
        page_copy.remove_logs()
        page_copy.delete_empty_blocks()
        page_copy.lower_assets_dir()
        page_copy.remove_image_alt_text()
        images = page_copy.get_all_images()
        image_paths = []
        for image in images:
            matches = re.findall(r'!\[.*?\]\((.*?)\)', image)
            for match in matches:
                if not os.path.isabs(match):
                    abs_path = os.path.abspath(os.path.join(self.get_logseq_dir(), match))
                    image_paths.append(abs_path)

        page_copy.set_file(os.path.join(self.get_logseq_dir(), tmp_filename))
        page_copy.write_to_file()
        html_content = pypandoc.convert_file(page_copy.get_file(), 'html', format='md')
        
        if css_file:
            with open(css_file, "r") as f:
                css_content = f.read()
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-csharp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-log.min.js"></script>
    
    <meta charset="UTF-8">
    <style>{css_content}</style>
</head>
<body>
    {html_content}
</body>
</html>"""    
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-nginx.min.js"></script> #doesnt work

        # Replace "sourceCode" with "language-" in the HTML content
        html_content = html_content.replace("sourceCode ", "language-")
        # Create a new directory with the same name as the filename (without extension)
        output_subdir = os.path.join(output_dir, page.get_page_name())
        os.makedirs(output_subdir, exist_ok=True)
        assets_subdir = os.path.join(output_dir, output_subdir, "assets")
        os.makedirs(assets_subdir, exist_ok=True)

        for image_path in image_paths:
            if os.path.exists(image_path):
                dest_path = os.path.join(assets_subdir, os.path.basename(image_path))
                with open(image_path, "rb") as src_file:
                    with open(dest_path, "wb") as dest_file:
                        dest_file.write(src_file.read())

        output_html = os.path.join(output_dir, output_subdir, f"{page.get_page_name()}.html")
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        # os.remove(page_copy.get_file())

        # Move the temporary markdown file to the output directory and rename it
        output_md = os.path.join(output_dir, output_subdir, f"{page.get_page_name()}.md")
        if os.path.exists(output_md):
            os.remove(output_md)
        os.rename(page_copy.get_file(), output_md)

        print(f"Converted {page.get_file()} to {output_html} with CSS styling.")
        

