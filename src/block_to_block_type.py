import re

def block_to_block_type(md_block): ### input: single markdown-block (a string)
    if re.findall(r"^#{1,6} (.+)", md_block):
        return "heading"
    
    elif re.findall(r"^```[\s\S]*?```$", md_block):
        return "code"
    
    elif re.findall(r"^(>).*$", md_block, re.MULTILINE):
        split_md_block = md_block.split("\n")
        for line in split_md_block:
            if line.startswith(">"):
                continue
            else:
                return "paragraph"
        return "quote"
    
    elif re.findall(r"^(?:\* |- ).*$", md_block, re.MULTILINE):
        return "unordered_list"
    
    elif re.findall(r"^(\d\. ).+$", md_block, re.MULTILINE):
        split_md_block = md_block.split("\n")
        for i, line in enumerate(split_md_block):
            if re.findall(rf"^{i+1}\. .+$", line):
                continue
            else:
                return "paragraph"
        return "ordered_list"
    
    else:
        return "paragraph"
