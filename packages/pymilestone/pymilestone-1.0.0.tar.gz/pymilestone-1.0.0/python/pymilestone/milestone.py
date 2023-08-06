# -*- coding: utf-8 -*-
"""
Module containing the class for the milestone.
"""

from pymilestone.element_type import ElementType


class Milestone():
    r"""
    Class for the milestone.
    
    
    Parameters
    ----------
    text : str
        Text of the milestone. Linebreaks must be added manually by
        inserting ``\n`` into the string.
        
    lines : int
        Number of lines. Defines the height of the milestone. Must be
        adjusted, if line breaks are added. Default is 2.
    """
    
    def __init__(self, text, lines=2):
        self.type = ElementType.MILESTONE
        """
        The element type.
        """
        
        self.text = text
        """
        Text of the milestone.
        """
        
        self.lines = lines
        """
        Number of lines.
        """
        
        self.key_date_list = []
        """
        List containing the dates for the respective keys.
        """
        
    def add_date(self, key, date):
        """
        Adds a date for a given category.
        
        Parameters
        ----------
        key : str
            Key of the respective category.
            
        date : datetime
            Date of the milestone.
        """
        
        self.key_date_list.append({
            'key': key,
            'date': date
        })
        
        return self


