# LogseqMdPy

A Python library designed to help you efficiently manage and manipulate your Logseq graphs. Provides tools and utilities for working with Logseq's markdown-based system.

## Disclaimer

This is an untested, unoptimized script that was made for personal use. I decided to let others use it if they want, but please do so at your own risk.

## Installation

To install the library, you can clone the repository and install the dependencies:

``` bash
git clone https://github.com/wolfj123/LogseqMdPy.git
cd LogseqMdPy
pip install -r requirements.txt
```

## Usage 


``` python

sys.path.append(os.path.abspath(r"path/to/LogseqMdPy"))
from LogseqMdPy.core import LogseqMdPy

# Initialize the LogseqMdPy object with the path to your Logseq directory
logseq = LogseqMdPy(r"path/to/your/logseq/directory")

# Example usage of the methods
logseq_dir = logseq.get_logseq_dir()
print(f"Logseq Directory: {logseq_dir}")

# Get a page by name
page = logseq.get_page_by_name("example_page_name")
if page:
    print(f"Page found: {page}")
else:
    print("Page not found")

# Get all files
all_files = logseq.get_all_files()
print(f"All files: {all_files}")

# Get all pages
all_pages = logseq.get_all_pages()
print(f"All pages: {all_pages}")

# Get all blocks with references
refs = ["example_ref"]
blocks_with_refs = logseq.get_all_blocks_with_refs(refs)
print(f"Blocks with refs: {blocks_with_refs}")

# Reset all cards of a page
logseq.reset_all_cards_of_page("example_page_name")

# Disable all cards of a page
logseq.disable_all_cards_of_page("example_page_name")

```
Make sure to replace "path/to/your/logseq/directory" and "example_page_name" with the actual path to your Logseq directory and the name of the page you want to work with.


## Acknowledgements
I recently discovered [another library the does similar things](https://github.com/thiswillbeyourgithub/LogseqMarkdownParser), so if this one doesn't satisfy you maybe check out [LogseqMarkdownParser](https://github.com/thiswillbeyourgithub/LogseqMarkdownParser)!


