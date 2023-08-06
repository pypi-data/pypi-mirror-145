# -*- coding: utf-8 -*-
"""
Module containing the class for the subcaption.
"""

from pymilestone._caption_base import _CaptionBase
from pymilestone.element_type import ElementType


class Subcaption(_CaptionBase):
    r"""
    Class for the subcaption.
    
    
    Parameters
    ----------
    text : str
        Text of the subcaption. Linebreaks must be added manually by
        inserting ``\n`` into the string.
        
    lines : int, optional
        Number of lines. Defines the height of the subcaption. Must be
        adjusted, if line breaks are added.
    """
    
    def __init__(self, text, lines=1):
        self.type = ElementType.SUBCAPTION
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

