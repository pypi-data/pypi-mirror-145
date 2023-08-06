# -*- coding: utf-8 -*-
"""
Module containing the class for the different categories of tasks and
milestones.
"""


class Category():
    """
    Class for the different categories of tasks and milestones.
    
    
    Parameters
    ----------
    key : str
        Key of the category. Can be chosen arbitrarily, but must be unique.
        
    displayname : str
        Displayname of the category, which will be displayed in the legend.
        
    color : Color
        A valid matplotlib color. Will be used to fill the respective
        bars (task) and diamonds (milestone).
        
    index : int
        Index of the category. Defines the line, on which the category
        is drawn. Allows to draw multiple categories in one line.
        Usually set to ``None``, so that each category is drawn on
        a separate line.
    """
        
    def __init__(self, key, displayname, color, index=None):
        self.key = key
        """
        Key of the category.
        """
        
        self.displayname = displayname
        """
        Displayname of the category.
        """
        
        self.color = color
        """
        Color of the category.
        """
        
        self.index = index
        """
        Index of the category defining the line, on which it is drawn.
        """
        


