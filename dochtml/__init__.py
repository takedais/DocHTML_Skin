"""DocHTML_Skin — データの杜 トーンで Markdown を HTML に変換"""
__version__ = "0.1.0"
from .converter import convert, parse_frontmatter

__all__ = ["convert", "parse_frontmatter", "__version__"]
