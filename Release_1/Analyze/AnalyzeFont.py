from pathlib import Path
from typing import Iterable, Any
from pdfminer.high_level import extract_pages

element = []
fontsize = []
fontstyle = []
dictt = {}
def TextAnalyze(filename_path):
    def show_ltitem_hierarchy(o: Any, depth=0):
        """Show location and text of LTItem and all its descendants"""

        fontstyle.append(get_optional_fontinfo(o))
        if isinstance(o, Iterable):
            for i in o:
                show_ltitem_hierarchy(i, depth=depth + 1)

    def get_indented_name(o: Any, depth: int) -> str:
        """Indented name of class"""
        return '  ' * depth + o.__class__.__name__

    def get_optional_fontinfo(o: Any) -> str:
        """Font info of LTChar if available, otherwise empty string"""
        if hasattr(o, 'fontname') and hasattr(o, 'size'):
            return f'{o.fontname} {round(o.size)}pt'
        return ''

    def get_optional_text(o: Any) -> str:
        """Text of LTItem if available, otherwise empty string"""
        if hasattr(o, 'get_text'):
            return o.get_text().strip()
        return ''

    path = Path(filename_path).expanduser()
    pages = extract_pages(path)
    show_ltitem_hierarchy(pages)

    font_info_dict = {}  

    for i in set(fontstyle):
        font_info = i.split(' ')
        if len(font_info) >= 2:
            font_size = round(float(font_info[-1][:-2]))  
            font_style = ' '.join(font_info[:-1]).lower()
            if font_style not in font_info_dict:
                font_info_dict[font_style] = [font_size]
            else:
                font_info_dict[font_style].append(font_size)

    return font_info_dict
