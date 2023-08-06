# -*- coding: utf-8 -*-
"""
Module containing the enumeration of the different elemen types
of the milestoneplan (caption, subcaption, task, milestione).
"""

from enum import Enum


class ElementType(str, Enum):
    """
    Enumeration of the different elemen types
    of the milestoneplan (caption, subcaption, task, milestione).
    """
    
    CAPTION = "CAPTION"
    """
    Caption.
    """
    
    SUBCAPTION = "SUBCAPTION"
    """
    Subcaption
    """
    
    TASK = "TASK"
    """
    Task.
    """
    
    MILESTONE = "MILESTONE"
    """
    Milestone.
    """
    
    
