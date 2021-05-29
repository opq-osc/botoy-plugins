import re


def clean_html(string):
    return re.sub(r"</?.+?/?>", "", string)
