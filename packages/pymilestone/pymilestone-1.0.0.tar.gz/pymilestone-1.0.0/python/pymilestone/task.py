# -*- coding: utf-8 -*-
"""
Module containing the class for a task.
"""

from pymilestone.element_type import ElementType


class Task():
    r"""
    Class for a task.
    
    
    Parameters
    ----------
    text : str
        Text of the task. Linebreaks must be added manually by
        inserting ``\n`` into the string.
        
    lines : int
        Number of lines. Defines the height of the task. Must be
        adjusted, if line breaks are added. Default is 2.
    """
    
    def __init__(self, text, lines=2):
        self.type = ElementType.TASK
        """
        The element type.
        """
        
        self.text = text
        """
        Text of the task.
        """
        
        self.lines = lines
        """
        Number of lines.
        """
        
        self.key_date_list = []
        """
        List containind the start and end date for a given key. Since it is
        a list, multiple date ranges can be added for the same key.
        """
        
    def add_date_range(self, key, start_date, end_date):
        """
        Adds a date range for the task. To add multiple date ranges
        for the same category, just call this method for each date range
        once, using the same key of the category.
        
        
        Parameters
        ----------
        key : str
            Key of the category.
            
        start_date : datetime
            Start date of the task.
            
        end_date : datetime
            End date of the task.
        """
        
        self.key_date_list.append({
            'key': key,
            'start_date': start_date,
            'end_date': end_date
        })
        
        return self


