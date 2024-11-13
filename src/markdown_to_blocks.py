def markdown_to_blocks(markdown):
    splitted_blocks = markdown.split("\n\n")
    clean_blocks = [block.strip() for block in splitted_blocks if block.strip() != ""]

    return clean_blocks