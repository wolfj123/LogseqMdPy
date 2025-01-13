import os

from LogseqMdPy.utils import name_to_filename
from LogseqMdPy.utils import get_card_props
from .models import LogseqPage

def get_page_by_name(name):
    name = name_to_filename(name)
    all_files = get_all_files()
    for file in all_files:
        base_name, extension = os.path.splitext(path)
        if base_name == name:
            return LogseqPage(file)
    return None

def get_all_files(pages = True, journals = True):
    """
    Gets a list of all file paths under the "pages" folder within the "journals" folder.

    This function assumes the following folder structure:

    - journals/
    - pages/  

    Returns:
        A list containing the absolute file paths of all files under the "pages" folder and the "journals" folder.
        An empty list is returned if the "journals" and "pages" folder is not found.
    """

    page_files = []
    folders = []

    if pages:
        pages_path = os.path.join(os.getcwd(),  "pages")
        folders.append(pages_path)
    if journals:
        journals_path = os.path.join(os.getcwd(), "journals")
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

def get_all_pages(pages = True, journals = True):
    all_pages = []
    for file in get_all_files(pages = pages, journals = journals):
        all_pages.append(LogseqPage(file))
    return all_pages

def get_all_blocks_with_refs(refs, include_inherited = True):
    result = []
    all_pages = get_all_pages()
    for page in all_pages:
        result = result + page.get_all_blocks_with_refs(refs, include_inherited)
    return result

def reset_all_cards_of_page(page_name):
    blocks = get_all_blocks_with_refs(["card", page_name])
    for b in blocks:
        b.delete_properties(get_card_props())
        p = b.get_page()
        p.write_to_file()

def disable_all_cards_of_page(page_name):
    blocks = get_all_blocks_with_refs(["card", page_name])
    for b in blocks:
        orig_text = b.get_text()
        if "#card" in orig_text and "#card-off" not in orig_text:
            new_text = orig_text.replace("#card", "#card-off")
            b.set_text(new_text)
        b.delete_properties(get_card_props())
        p = b.get_page()
        p.write_to_file()
