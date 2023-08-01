import re

def markdown_to_bbcode(markdown_text):
    # Regular expressions to match Markdown elements
    bold_regex = r'\*\*(.*?)\*\*'
    italic_regex = r'\*(.*?)\*'
    code_regex = r'`([^`]+)`'
    header_regex = r'^(#+)\s*(.*?)$'
    unordered_list_regex = r'^\s*[-*]\s+(.*?)$'
    ordered_list_regex = r'^\s*\d+\.\s+(.*?)$'
    link_regex = r'\[([^\]]+)\]\(([^\)]+)\)'

    # Dictionary to hold the translations of Markdown to BBCODE elements
    markdown_to_bbcode = {
        bold_regex: r'[b]\1[/b]',
        italic_regex: r'[i]\1[/i]',
        code_regex: r'[code]\1[/code]',
        header_regex: lambda match: f"[center][color=#f1c232][size={7 - len(match.group(1))}][b]{match.group(2)}[/b][/size][/color][/center]",
        unordered_list_regex: r'[*]\1',
        ordered_list_regex: lambda match: f"[#]{match.group(1)}",
        link_regex: r'[url=\2]\1[/url]',
    }

    # Applying the regular expressions for translation
    bbcode_text = markdown_text
    for markdown_regex, bbcode_replacement in markdown_to_bbcode.items():
        if callable(bbcode_replacement):
            bbcode_text = re.sub(markdown_regex, bbcode_replacement, bbcode_text, flags=re.MULTILINE)
        else:
            bbcode_text = re.sub(markdown_regex, bbcode_replacement, bbcode_text)

    return bbcode_text

import os

if __name__ == "__main__":
    # iterate over .md files in the in directory
    for filename in os.listdir("in"):
        if filename.endswith(".md"):
            with open(os.path.join("in", filename), "r") as f:
                markdown_text = f.read()
                bbcode_text = markdown_to_bbcode(markdown_text)
                bbcode_lines = bbcode_text.split("\n")
                
                is_list = False
                for i in range(len(bbcode_lines)):
                    # match line with images
                    img_pattern = r'\!\[url=([^\]]+\.(?:gif|png|jpg))\]([^/]+)\[/url\]'
                    if re.match(img_pattern, bbcode_lines[i]):
                        image_url = re.search(img_pattern, bbcode_lines[i]).group(1)
                        print(image_url)
                        # change to [img]https://raw.githubusercontent.com/D7ry/wheeler/main/images/item_usage.gif[/img]
                        modified_img_string = f"[center][img]https://raw.githubusercontent.com/D7ry/wheeler/main/{image_url}[/img][/center]"
                        bbcode_lines[i] = modified_img_string
                        if i < len(bbcode_lines) - 1: # this assumes that for every image, we have a italicized caption one line below
                            bbcode_lines[i+1] = f"[center]{bbcode_lines[i+1]}[/center]"

                # write to .bb file in the out directory
                bbcode_text = "\n".join(bbcode_lines)
                with open(os.path.join("out", filename[:-3] + ".bb"), "w") as out_file:
                    out_file.write(bbcode_text)
