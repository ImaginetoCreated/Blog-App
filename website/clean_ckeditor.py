# import bleach - sanitize the user input in the CKEditor to
# prevent XSS attacks, ensure the validity of the HTML data and prevent
# sql injection attacks

import bleach
from flask import request

## strips invalid tags/attributes
def strip_invalid_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']

    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }

    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)

    return cleaned






# AI generated
# import re
# from urlparse import urljoin
# from BeautifulSoup import BeautifulSoup, Comment
#
#
# def sanitizeHtml(value, base_url=None):
#     # Regex patterns to match JavaScript and VBScript
#     rjs = r'[\\s]*(&#x.{1,7})?'.join(list('javascript:'))
#     rvb = r'[\\s]*(&#x.{1,7})?'.join(list('vbscript:'))
#     re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
#
#     # List of valid tags and attributes
#     validTags = 'p i strong b u a h1 h2 h3 pre br img'.split()
#     validAttrs = 'href src width height'.split()
#     urlAttrs = 'href src'.split()  # Attributes which should have a URL
#
#     # Parse the input with BeautifulSoup
#     soup = BeautifulSoup(value)
#
#     # Remove comments
#     for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
#         comment.extract()
#
#     # Remove invalid tags and attributes
#     for tag in soup.findAll(True):
#         if tag.name not in validTags:
#             tag.hidden = True
#         attrs = tag.attrs
#         tag.attrs = []
#         for attr, val in attrs:
#             if attr in validAttrs:
#                 val = re_scripts.sub('', val)  # Remove scripts (vbs & js)
#                 if attr in urlAttrs:
#                     val = urljoin(base_url, val)  # Calculate the absolute url
#                 tag.attrs.append((attr, val))
#
#     # Return the sanitized HTML
#     return soup.renderContents().decode('utf8')

