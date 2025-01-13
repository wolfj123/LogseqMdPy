import os
import re
from .utils import filename_to_name, count_leading_tabs, get_reference_pattern, get_tag_pattern, get_tag_ref_pattern

class LogseqBlock:
    """
    A class representing a block in a logseq page.
    """
    def __init__(self):
        """
        Initializes an empty block.
        """
        self.page = None
        self.text = ""
        self.parent = []
        self.children = []
        self.properties = {}
        self.refs = []
        self.refs_inherited = []
    
    def get_height(self):
        result = 1
        max_child_result = 0
        for child in self.get_children():
            curr_child_result = child.get_height()
            if curr_child_result > max_child_result:
                max_child_result = curr_child_result
        return result + max_child_result

    def get_block_tree_size(self):
        result = 1
        for child in self.get_children():
            result = result + child.get_block_tree_size()
        return result

    def get_page(self):
        return self.page

    def set_page(self, page):
        page_name = page.get_page_name()
        self.refs_inherited.append(page_name)
        self.page = page

    def get_text(self):
        return self.text

    def get_refs(self):
        return self.refs

    def get_properties(self):
        return self.properties

    def delete_properties(self, properties):
        text = self.get_text()
        for property in properties:
            new_text = re.sub(r"(\t)*( )*" + property + r"::(.*)((\n)+|$)", "", text)
            text = new_text

        self.set_text(text)

    def set_text(self, text):
        self.refs = []
        self.text = text

        # props
        for line in text.splitlines():
            if re.search(r"[a-zA-Z0-9]+::(.*)", line):
                if not "{" in line:
                    split = line.split("::", maxsplit = 1)
                    prop = split[0].lstrip()
                    values_unstripped = split[1].split(",")
                    values = []
                    for val in values_unstripped:
                        values.append(val.strip())
                    self.properties[prop.lower()] = values 

        # refs
        match1 = re.findall(get_reference_pattern(), text)
        match2 = re.findall(get_tag_ref_pattern(), text)
        match3 = re.findall(get_tag_pattern(), text)
        if match1:
            self.refs = self.refs + match1
        if match2:
            self.refs = self.refs + match2
        if match3:
            self.refs = self.refs + match3
    
    def get_all_blocks(self):
        result = []
        result.append(self)
        for child in self.get_children():
            result = result + (child.get_all_blocks())
        return result

    def has_pattern(self, pattern):
        """
        Searchings for reg exp pattern in the block or its sub-blocks
        If found, returns the block(s) that contain the pattern in their text

        Returns a list of all blocks containing the pattern.
        """

        result = []
        text = self.get_text()
        if text:
            matches = None
            try:
                matches = re.findall(pattern, text)
            except Exception as e:
                print(e)
                print(text + "\n")
                print(pattern + "\n")
                exit()

            if matches:
                for match in matches:
                    # print(match)
                    result.append((self, match))
        child_blocks = self.get_children()
        for child_block in child_blocks:
            result = result + child_block.has_pattern(pattern)
        return result

    def add_child(self, child_block):
        if child_block == self:
            print("error")
        if child_block not in self.children:
            self.children.append(child_block)
            child_block.parent = self

    def set_parent(self, new_parent):
        if self not in new_parent.get_children():
            new_parent.children.append(self)
            self.parent = new_parent
            for ref in self.parent.refs:
                if ref not in self.refs_inherited:
                    self.refs_inherited.append(ref)
            for ref in self.parent.refs_inherited:
                if ref not in self.refs_inherited:
                    self.refs_inherited.append(ref)

    def get_parent(self):
        return self.parent
    
    def get_path(self):
        path = []
        curr_node = self
        parent = self.get_parent()
        while parent:
            path.insert(0, curr_node)
            curr_node = parent
            parent = curr_node.get_parent()
        return path

    def get_children(self):
        return self.children

    def collapse(self, collapse):
        orig_text = self.get_text()
        new_text = ""
        if collapse:
            new_text = orig_text + "\n  collapsed:: true"
        else:
            new_text = orig_text.replace("collapsed:: true", "")
        self.set_text(new_text)

    def to_text(self, depth = 0):
        result = ("\t" * depth) + "- " + self.get_text()
        if len(self.get_children()) > 0:
            for child_block in self.get_children():
                result = result + "\n" + child_block.to_text(depth + 1)
        return result

    def get_all_blocks_with_refs(self, refs, include_inherited_refs = True):
        result = []
        refs_to_check = []
        for r in self.refs:
            refs_to_check.append(r)
        if include_inherited_refs:
            for r in self.refs_inherited:
                refs_to_check.append(r)

        all_refs_found = True
        for ref in refs:
            if ref not in refs_to_check:
                all_refs_found = False
        if all_refs_found:
            result.append(self)
        for child in self.get_children():
            result = result + child.get_all_blocks_with_refs(refs, include_inherited_refs)
        return result


class LogseqPage:
    """
    A class representing a node in a tree structure.
    """
    def __init__(self, filename):
        """
        Initializes a TreeNode object.

        Args:
        data: The data to be stored in the node.
        """
        self.filename = filename
        path_with_no_extention, extension = os.path.splitext(filename)
        self.name = filename_to_name(os.path.basename(path_with_no_extention))
        normalized_path = os.path.normpath(filename)
        path_list = normalized_path.split("\\")
        last_folder = path_list[-2]
        self.is_journal = last_folder == "journals"
        self.blocks = []
        self.properties = {} # page props are the props from the top block

        with open(filename, 'r', encoding="utf-8") as file:
            blocks_by_depth = [[]]
            current_depth = 0
            lines = []
            try:
                lines = file.readlines()
            except Exception as e:
                print(filename)
                print(e)
                exit()

            i = 0
            while i < len(lines):
                line = lines[i]

                # Normal block
                current_depth = count_leading_tabs(line)
                new_block = LogseqBlock()
                new_block.set_page(self)
                
                # Text
                text = ""
                if line.lstrip().startswith("-"):
                    split = (line.split("-", maxsplit=1)) 
                    if len(split) > 0:
                        text = split[1].lstrip()
                    else:
                        text = ""
                else:
                    text = line
                if i < len(lines) - 1:
                    j = 1
                    next_line = lines[i + j]
                    while not next_line.lstrip().startswith("-"):
                        text += next_line
                        j += 1
                        if i + j == len(lines):
                            break
                        next_line = lines[i + j]
                    j -= 1
                    i = i + j
                new_block.set_text(text.rstrip())

                # Add new block to block list
                if len(blocks_by_depth) <= current_depth:
                    blocks_by_depth.append([new_block])
                else:
                    blocks_by_depth[current_depth].append(new_block)

                # Parent
                if current_depth > 0:
                    parent = blocks_by_depth[current_depth-1][-1]
                    new_block.set_parent(parent)
                i += 1
    
        for depth_0_block in blocks_by_depth[0]:
            self.blocks.append(depth_0_block)
        
    def get_page_name(self):
        return self.name

    def get_file(self):
        return self.filename

    def is_journal(self):
        return self.is_journal

    def get_blocks(self):
        return self.blocks

    def get_properties(self):
        if len(self.get_blocks()) > 0:
            return self.blocks[0].get_properties()
        else:
            return {}

    def to_text(self):
        result = ""
        is_first = True
        for block in self.get_blocks():
            if is_first:
                result += block.to_text()
            else:
                result += "\n" + block.to_text()
            is_first = False
        return result

    def has_pattern(self, pattern):
        result = []
        for block in self.get_blocks():
            blocks_with_pattern = block.has_pattern(pattern)
            result = result + blocks_with_pattern
        return result

    def write_to_file(self):
        text = self.to_text()
        with open(self.get_file(), 'w+', encoding="utf-8") as out_file:
            out_file.write(text)

    def get_all_prop_refs(self):
        result = []
        for prop in self.get_properties():
            for val in self.get_properties()[prop]:
                match1 = re.findall(get_reference_pattern(), val)
                match2 = re.findall(get_tag_ref_pattern(), val)
                match3 = re.findall(get_tag_pattern(), val)
                if match1:
                    result.append((prop, match1[0])) 
                    continue 
                if match2:
                    result.append((prop, match2[0])) 
                    continue 
                if match3:
                    result.append((prop, match3[0])) 
                    continue 
        return result

    def get_all_references_in_blocks(self):
        all_refs = self.has_pattern(get_reference_pattern())
        all_tags = self.has_pattern(get_tag_pattern())
        all_tag_refs = self.has_pattern(get_tag_ref_pattern())
        result = all_refs + all_tags + all_tag_refs
        return result

    def get_all_blocks_with_refs(self, refs, include_inherited_refs = True):
        result = []
        for block in self.get_blocks():
            result = result + block.get_all_blocks_with_refs(refs, include_inherited_refs)
        return result
