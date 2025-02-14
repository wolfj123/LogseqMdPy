import os

from LogseqMdPy.utils import *
from LogseqMdPy.graph import *
from .models import LogseqPage, LogseqBlock

class LogseqMdPy:
    def __init__(self, logseq_directory):
        self.logseq_dir = logseq_directory

    def get_logseq_dir(self):
        return self.logseq_dir

    def get_page_by_name(self, name):
        name = name_to_filename(name)
        all_files = self.get_all_files()
        for file in all_files:
            base_name, extension = os.path.splitext(file)
            if base_name == name:
                return LogseqPage(file)
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