__version__ = '0.5.4'

import markdown as md

from .citation import citation
from .video import video


def marquedown(document: str, **kwargs):
    """Convert both Marquedown and Markdown into HTML."""

    if kwargs.get('citation', True):
        document = citation(document)

    if kwargs.get('video', True):
        document = video(document)
        
    html = md.markdown(document)

    return html