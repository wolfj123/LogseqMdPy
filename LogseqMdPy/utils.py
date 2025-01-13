import re
# import os

name_to_filename_map = {
    ":" : "%3",
    "\"" : "%22",
    "\\" : "%2",
    "?" : "%3F"
}

filename_to_name_map = {
    "%3F" : "?",
    "%3" : ":",
    "%22" : "\"",
    "%2" : "\\" 
}

card_properties = ["card-last-interval", "card-repeats", "card-ease-factor", "card-next-schedule", "card-last-reviewed", "card-last-score"]

def get_card_props():
    return card_properties

# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# try:
#     os.chdir(parent_dir)
#     # print(f"Successfully changed directory to: {parent_dir}")
# except OSError as e:
#     print(f"Error changing directory: {e}")


reference_pattern = r"\[\[(.*?)\]\]"
def get_reference_pattern():
    return reference_pattern

tag_pattern = r"(?<!\[)#(\w+)"
def get_tag_pattern():
    return tag_pattern

tag_ref_pattern = r"#\[\[(.*?)\]\]"
def get_tag_ref_pattern():
    return tag_ref_pattern

def name_to_filename(name):
    for char in name_to_filename_map:
        name = name.replace(char, name_to_filename_map[char])
    return name

def filename_to_name(name):
    for char in filename_to_name_map:
        name = name.replace(char, filename_to_name_map[char])
    return name

def count_leading_tabs(text):
  """
  Counts the number of leading tabs ("\t") in a string.

  Args:
      text: The string to check.

  Returns:
      The number of leading tabs in the string.
  """
  count = 0
  for char in text:
    if char == "\t":
      count += 1
    else:
      break  # Stop counting once a non-tab character is found
  return count

def sanitize_filename(filename):
    """Sanitizes a filename by replacing invalid characters with underscores.

    Args:
        filename: The filename to sanitize.

    Returns:
        The sanitized filename.
    """
    pattern = r"[^\w\-_\. ]{1,}"  # Match one or more characters that are not alphanumeric, underscore, hyphen, dot, or space
    replacement = "_"
    return re.sub(pattern, replacement, filename)   

def h(text, n):
    return "#" * n + " " + text

def bold(text):
    return "** " + text + " **"

def italic(text): 
    return "* " + text + " *"

def tag(text): 
    if " " in text and (not is_page_ref(text)):
        return "#[[" + text.strip() + "]]"
    else:
        return "#" + text.strip()

def is_page_ref(text):
    text = text.strip()
    return text.startswith("[[") and text.endswith("]]")

def page_ref(text):
    return "[[" + text + "]]"