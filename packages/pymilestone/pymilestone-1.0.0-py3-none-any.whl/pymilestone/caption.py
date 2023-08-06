# -*- coding: utf-8 -*-
"""
Module containing the class for the Caption.
"""

from pymilestone._caption_base import _CaptionBase
from pymilestone.element_type import ElementType


class Caption(_CaptionBase):
    r"""
    Class for the caption.
    
    
    Parameters
    ----------
    text : str
        Text of the caption. Linebreaks must be added manually by
        inserting ``\n`` into the string.
        
    lines : int, optional
        Number of lines. Defines the height of the caption. Must be
        adjusted, if line breaks are added.
    """
    
    def __init__(self, text, lines=1):
        self.type = ElementType.CAPTION
        """
        The element type.
        """
        
        self.text = text
        """
        Text of the caption.
        """
        
        self.lines = lines
        """
        Number of lines. Defines the height of the caption.
        """
        


