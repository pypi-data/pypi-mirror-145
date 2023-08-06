# -*- coding: utf-8 -*-
"""
Module containing the class for the milestone plan.
"""

from datetime import datetime
from dateutil.rrule import rrule, DAILY
from dateutil.relativedelta import relativedelta
import calendar
import matplotlib.pyplot as plt
import locale

from pymilestone import _CaptionBase, Caption, Subcaption, Milestone, Task
from pymilestone.util import set_fig_size, get_data_list


class Milestoneplan():
    """
    Main class for the milestone plan.
    
    
    Parameters
    ----------
    include_weekend : boolean
        Defines, whether the weekend (Saturday, Sunday) are shown as a
        separate day. If both are not workdays, it is better, to
        set this value to ``False``, so that for tasks ending on a friday,
        the end date will mark the end of the week.
        
    today : datetime
        Date, at which to show the red line. If ``None``, no red line
        is shown. If set, the red line will be shown at the respective
        date.
        
    custon_locale : str
        Locale to define the language of the milestoneplan. Is important,
        if month names are shown. If not 
        
    kwargs
        Additional keyword arguments for further customization. Following
        keys can be used.
        
        +---------------------------------------+---------------+-----------------------------------------------+
        | Key                                   | Type          | Description                                   |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``c_background_top_caption``          | Color         | Background color of the top caption.          |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``c_background_top_subcaption``       | Color         | Background color of the top sub caption.      |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``c_background_task_caption``         | Color         | Background color of the task captions.        |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``c_background_task_subcaption``      | Color         | Background color of the tast sub captions.    |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``end_date``                          | datetime      | Last day of the milestone plan. If not        |
        |                                       |               | provided, it will be determined               |
        |                                       |               | automatically from the given tasks and        |
        |                                       |               | configuration.                                |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``fs_top_caption``                    | int           | Font size of the top caption.                 |
        |                                       |               | Default is 12.                                |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``fs_top_subcaption``                 | int           | Font size of the top sub caption.             |
        |                                       |               | Default is 8.                                 |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``fs_task``                           | int           | Font size of the task. Is also the font       |
        |                                       |               | size of the tast caption, task sub caption,   |
        |                                       |               | and milestone. Default is 10.                 |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``fs_legend``                         | int           | Font size of the legend. Default is 10.       |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``key_top_caption``                   | str           | Defines, what is shown in the top caption.    |
        |                                       |               | Choises are                                   |
        |                                       |               |                                               |
        |                                       |               |     - ``"year"`` (shows the year),            |
        |                                       |               |     - ``"month"`` (shows the month).          |
        |                                       |               |                                               |
        |                                       |               | Default is ``"month"``.                       |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``key_sub_caption``                   | str           | Defines, what is shown in the top sub         |
        |                                       |               | caption. Choises are                          |
        |                                       |               |                                               |
        |                                       |               |     - ``"week"`` (shows the calendar week),   |
        |                                       |               |     - ``"month"`` (shows the month),          |
        |                                       |               |     - ``"quarter"`` (shows the quarter),      |
        |                                       |               |                                               |
        |                                       |               | Default is ``"month"``.                       |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``start_date``                        | datetime      | First day of the milestone plan. If not       |
        |                                       |               | provided, it will be determined               |
        |                                       |               | automatically from the given tasks and        |
        |                                       |               | configuration.                                |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``width_col_task``                    | float         | Width of the column with the tasks.           |
        |                                       |               | Default is 3.5.                               |
        +---------------------------------------+---------------+-----------------------------------------------+
        | ``width_day``                         | float         | Defines the width of each single day and      |
        |                                       |               | hence the width of the entire milestone       |
        |                                       |               | plan.                                         |
        +---------------------------------------+---------------+-----------------------------------------------+
    
    
    Examples
    --------
    Examples of usage can be found here:
    :ref:`tutorial`.
        
    """  # noqa: E501
    
    def __init__(self, include_weekend=True, today=None, custom_locale=None,
                 **kwargs):
        self.task_list = []
        """
        List of the Elements. Can contain Captions, Sub captions, Tasks,
        and Milestones.
        """
        
        self.category_dict = {}
        """
        Dictionary holding the data for the categories.
        """
        
        # read the parameters
        self.include_weekend = include_weekend
        self.today = today
        
        # set language
        if(custom_locale is not None):
            locale.setlocale(locale.LC_ALL, custom_locale)
        
        # read colors
        self.c_background_top_caption = kwargs.get(
            'c_background_top_caption', (153 / 255, 204 / 255, 255 / 255))
        self.c_background_top_subcaption = kwargs.get(
            'c_background_top_subcaption', (1.0, 1.0, 1.0))
        self.c_background_task_caption = kwargs.get(
            'c_background_task_caption', (0.7, 0.7, 0.7))
        self.c_background_task_subcaption = kwargs.get(
            'c_background_task_subcaption', (0.9, 0.9, 0.9))
        
        # get font sizes
        self.fs_top_caption = kwargs.get('fs_top_caption', 12)
        self.fs_top_subcaption = kwargs.get('fs_top_subcaption', 8)
        self.fs_task = kwargs.get('fs_task', 10)
        self.fs_legend = kwargs.get('fs_legend', 10)
        
        # get width of the first column
        self.width_col_task = kwargs.get('width_col_task', 3.5)
        
        # get the keys for the top caption and top sub caption
        self.key_top_caption = kwargs.get('key_top_caption', 'month')
        self.key_sub_caption = kwargs.get('key_sub_caption', 'week')
        
        # factor to convert the units on the axis into inces
        self.fac_dim_to_inch = 0.125
        self.fac_inch_to_dim = 1 / self.fac_dim_to_inch
        
        # automatically determine width of one day
        self.width_day = kwargs.get('width_day', None)
        if(self.width_day is None):
            self.width_day = max(self.fs_top_caption / 30, 
                                 self.fs_top_subcaption / 30)
        
        # get start and end date
        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)
        
    def add_element(self, elem):
        """
        Adds an element (Caption, Sub caption, Task, Milestone) to the list.
        
        
        Parameters
        ----------
        elem : object
            Element to add. Must be either ``Caption``, ``Subcaption``, 
            ``Task``, or ``Milestone``.
        """
        
        self.task_list.append(elem)
        
    def add_category(self, elem):
        """
        Adds a category to the dictionary.
        
        
        Parameters
        ----------
        elem : Category
            Category to add. The key must be unique, it is obtained from the
            given object.
        """
        
        key = elem.key
        
        # check, if key already exsists
        if key in self.category_dict:
            raise ValueError("Category with key {key} already added!")
        
        # set element index
        # TODO: this does not work, if user set the index manually
        # in previously added categories
        if(elem.index is None):
            elem.index = len(self.category_dict)
        
        # save category
        self.category_dict[key] = elem
        
    def create_fig(self, pad=0.1):
        """
        Renders the Milestoneplan.
        
        
        Parameters
        ----------
        pad : float
            Pad around the milestoneplan.
            
        
        Returns
        -------
        fig : Figure
            Matplotlib figure, on which the milestoneplan was plotted.
        """
        
        # 1. define some values
        
        # position of the first two vertical lines
        x_left = 0
        x0 = self.width_col_task * self.fac_inch_to_dim
        
        # position of the first horizontal lines
        y_top = 39
        y_line1 = y_top
        y_line2 = y_top - 1.75 * self.fs_top_caption / 72 * self.fac_inch_to_dim  # noqa: E501
        y_line3 = y_line2 - 1.75 * self.fs_top_subcaption / 72 * self.fac_inch_to_dim  # noqa: E501
        
        # linewidths
        # TODO: maybe parameter?
        lw_bold = 2
        lw_fine = 0.75
        
        #######################################################################
        
        # 2. get start and end date
        date_list = []
        
        # 2.1 iterate over each added element
        for task_config in self.task_list:
            # captions and subcaptions do not have a date
            if(isinstance(task_config, _CaptionBase)):
                continue
            
            # save start and end date of task
            elif(isinstance(task_config, Task)):
                for d in task_config.key_date_list:
                    date_list.append(d['start_date'])
                    date_list.append(d['end_date'])
            
            # save date of milestone
            elif(isinstance(task_config, Milestone)):
                for d in task_config.key_date_list:
                    date_list.append(d['date'])
                    
            else:
                raise ValueError(
                    f"Invalid type of task_config: {task_config.task_type}")
        
        # 2.2. get maximum and minimum date
        start_date_tmp = min(date_list)
        end_date_tmp = max(date_list)
        
        # 2.3. obtain start and end date (if not already given by the user)
        # if year is selected, use full years
        if(self.start_date is None):
            if(self.key_top_caption == 'year'):
                self.start_date = datetime(
                    start_date_tmp.year, 1, 1)
                
            else:
                self.start_date = datetime(
                    start_date_tmp.year, start_date_tmp.month, 1)
                
        if(self.end_date is None):
            if(self.key_top_caption == 'year'):
                self.end_date = datetime(end_date_tmp.year, 12, 31) 
                
            else:
                self.end_date = (
                    datetime(end_date_tmp.year, end_date_tmp.month, 1) 
                    + relativedelta(months=+1) + relativedelta(days=-1)
                )
        
        #######################################################################
        
        # 3. divide the time period between start and end date into
        # smaller chuncks of periods (e.g. months, weeks, quarters)
        i_date_dict = {}
        
        # indices, when the given day starts and ends
        date_data_list = []
        
        i_date = -1
        
        # 3.1. iterate over each day between start and end
        for date in rrule(DAILY, dtstart=self.start_date, until=self.end_date):
            year_tmp = date.year
            month_tmp = date.month
            week_tmp = date.isocalendar()[1]
            dow = date.weekday()
            quarter_tmp = (month_tmp - 1) // 3  # 0-based
            
            key_date = date.strftime("%Y%m%d")

            if(self.include_weekend
               or dow not in [5, 6]):
                i_date += 1

                date_data_list.append({
                    'year': year_tmp,
                    'month': month_tmp,
                    'week': week_tmp,
                    'quarter': quarter_tmp
                })
    
                i_date_dict[key_date] = (i_date, i_date + 1)
            
            else:
                # push saturday and sunday to the end of the week,
                # if weekend is not included
                i_date_dict[key_date] = (i_date + 1, i_date + 1)
                
        # 3.2. divide time period into chuncks
        year_data_list = get_data_list(date_data_list, 'year')
        month_data_list = get_data_list(
            date_data_list, 'month', name_list=calendar.month_name)
        week_data_list = get_data_list(date_data_list, 'week')
        quarter_data_list = get_data_list(
            date_data_list, 'quarter', ["Q1", "Q2", "Q3", "Q4"])
        
        # 3.3. save data into respective variables, depending
        # on the selection of the top caption and top sub caption
        if(self.key_top_caption == 'year'):
            top_caption_list = year_data_list
            
        elif(self.key_top_caption == 'month'):
            top_caption_list = month_data_list
            
        else:
            raise ValueError(
                "Invalid value for key_top_caption: {self.key_top_caption}")
            
        if(self.key_sub_caption == 'week'):
            sub_caption_list = week_data_list
            
        elif(self.key_sub_caption == 'month'):
            sub_caption_list = month_data_list
            
        elif(self.key_sub_caption == 'quarter'):
            sub_caption_list = quarter_data_list
            
        else:
            raise ValueError(
                "Invalid value for key_sub_caption: {self.key_sub_caption}")

        #######################################################################
        
        # 4. do the plotting
        
        # ---------------------------------------------------------------------
        # 4.1. create the figure and the axis
        fig = plt.figure()
        ax = fig.gca()
        
        ax.set_aspect('equal')
        
        # ---------------------------------------------------------------------
        # 4.2. plot top caption
        x_start_top_caption = x0
        
        for i_data, data_dict in enumerate(top_caption_list):
            # 4.2.1. get data
            displayname = data_dict['displayname']
            days = data_dict['days']
            
            # 4.2.2. get width
            width_month = self.width_day * days
            x_end_top_caption = x_start_top_caption + width_month
            
            # 4.2.3. plot text
            y_baseline = y_line2 + 0.5 * self.fs_top_caption / 72 * self.fac_inch_to_dim  # noqa: E501
            
            ax.text(0.5 * (x_start_top_caption + x_end_top_caption), 
                    y_baseline, displayname, color='k', 
                    ha='center', va='baseline', fontsize=self.fs_top_caption)
            
            x_start_top_caption = x_end_top_caption
            
        # position of the most right vertical line
        x_right = x_end_top_caption
        
        # ---------------------------------------------------------------------
        # 4.3. print top sub caption
        x_start_week_caption = x0
        for i_data, data_dict in enumerate(sub_caption_list):
            # 4.3.1. get data
            displayname = data_dict['displayname']
            days = data_dict['days']
            
            # 4.3.2. get width
            width_week = self.width_day * days
            x_end_week_caption = x_start_week_caption + width_week
            
            # 4.3.3. plot text
            y_baseline = y_line3 + 0.5 * self.fs_top_subcaption / 72 * self.fac_inch_to_dim  # noqa: E501
            
            if(self.include_weekend and days == 7
               or days == 5 or self.key_sub_caption in ['quarter', 'month']):
                # do not plot week number if it is not a full week
                ax.text(0.5 * (x_start_week_caption + x_end_week_caption), 
                        y_baseline, displayname, color='k', 
                        ha='center', va='baseline', 
                        fontsize=self.fs_top_subcaption)
            
            x_start_week_caption = x_end_week_caption
    
        # ---------------------------------------------------------------------
        # 4.4. plot the background of the top caption and the top sub caption
        
        ax.fill_between([x_left, x_right],
                        [y_line1, y_line1],
                        [y_line2, y_line2],
                        lw=0.0,
                        color=self.c_background_top_caption)
        
        ax.fill_between([x_left, x_right],
                        [y_line2, y_line2],
                        [y_line3, y_line3],
                        lw=0.0,
                        color=self.c_background_top_subcaption)
        
        # ---------------------------------------------------------------------
        # 4.5. plot the elements (Caption, Subcaption, Task, Milestone)
        
        y_line_top = y_line3
    
        # iterate over each element
        for task_config in self.task_list:
            # 4.5.1. plot caption
            if(isinstance(task_config, _CaptionBase)):
                # get data
                lines = task_config.lines
                
                # bold font requires special treatment, if tex is enabled
                if(plt.rcParams['text.usetex']):
                    s = r"\textbf{{{}}}".format(task_config.text)
                    s_weight = None
                
                else:
                    s = task_config.text
                    s_weight = 'bold'
                
                # get height of the line
                height = 1.4 * (self.fs_task / 72 * self.fac_inch_to_dim) * lines  # noqa: E501
                y_line_bottom = y_line_top - height
                
                # get background color
                if(isinstance(task_config, Caption)):
                    c_background = self.c_background_task_caption
                elif(isinstance(task_config, Subcaption)):
                    c_background = self.c_background_task_subcaption
                else:
                    raise ValueError(
                        "Invalid type of task_config:"
                        f" {task_config.task_type}")
                
                # plot the text
                ax.text(x_left + 0.5, 0.5 * (y_line_top + y_line_bottom) - 0.2,
                        s, color='k', ha='left', va='center', 
                        fontsize=self.fs_task, weight=s_weight)
                # plot the bottom line
                ax.plot([x_left, x_right], [y_line_bottom, y_line_bottom], 
                        '-', color='k', 
                        linewidth=lw_fine)
                
                # plot the background
                ax.fill_between([x_left, x_right],
                                [y_line_top, y_line_top],
                                [y_line_bottom, y_line_bottom],
                                lw=0.0,
                                color=c_background)
                
                y_line_top = y_line_bottom
            
            # 5.4.2. plot the task
            elif(isinstance(task_config, Task)):
                # get data
                lines = task_config.lines
                s = task_config.text
                
                # get height of the line
                height = 1.4 * (self.fs_task / 72 * self.fac_inch_to_dim) * lines  # noqa: E501
                y_line_bottom = y_line_top - height
                
                # get height of each category
                key_date_list = task_config.key_date_list
                height_time_config = height / len(self.category_dict.keys())
                
                # plot the text
                ax.text(x_left + 0.5, 0.5 * (y_line_top + y_line_bottom) - 0.2,
                        s, color='k', ha='left', va='center', 
                        fontsize=self.fs_task)
                
                # plot the bottom line
                ax.plot([x_left, x_right], [y_line_bottom, y_line_bottom], 
                        '-', color='k', 
                        linewidth=lw_fine)
                
                # plot each time range
                for time_config in key_date_list:
                    # get data
                    key = time_config['key']
                    start_date = time_config['start_date']
                    end_date = time_config['end_date']
                    
                    # get index of start and end date
                    i_start_date = i_date_dict[
                        start_date.strftime("%Y%m%d")][0]
                    i_end_date = i_date_dict[end_date.strftime("%Y%m%d")][1]
                    
                    # get further data
                    color = self.category_dict[key].color
                    i_category = self.category_dict[key].index
                    
                    # get start and end positions
                    x_start = x0 + i_start_date * self.width_day
                    x_end = x0 + i_end_date * self.width_day
                    
                    # get top and bottom y position
                    y1 = y_line_top - i_category * height_time_config
                    y2 = y1 - height_time_config
                    
                    # plot bar
                    x_list = [x_start, x_end]
                    y1_list = [y1, y1]
                    y2_list = [y2, y2]
                    ax.fill_between(x_list, y1_list, y2_list, color=color, 
                                    lw=0.0)
                    
                y_line_top = y_line_bottom
            
            # 4.5.3. plot milestone
            elif(isinstance(task_config, Milestone)):
                # get data
                lines = task_config.lines
                s = task_config.text
                
                # get height of the line
                height = 1.4 * (self.fs_task / 72 * self.fac_inch_to_dim) * lines  # noqa: E501
                y_line_bottom = y_line_top - height
                
                # get height of each category
                key_date_list = task_config.key_date_list
                height_time_config = height / len(self.category_dict.keys())
    
                # plot the text
                ax.text(x_left + 0.5, 0.5 * (y_line_top + y_line_bottom) - 0.2,
                        s, color='k',
                        ha='left', va='center', fontsize=self.fs_task)
                
                # plot the bottom line
                ax.plot([x_left, x_right], [y_line_bottom, y_line_bottom], 
                        '-', color='k', 
                        linewidth=lw_fine)
            
                # plot each date
                for time_config in key_date_list:
                    # get data
                    key = time_config['key']
                    date = time_config['date']
                    
                    # get index of date
                    i_date = i_date_dict[date.strftime("%Y%m%d")][1]
                    
                    # get further data
                    color = self.category_dict[key].color
                    i_category = self.category_dict[key].index
                    
                    # get top, left, bottom, right position of the diamond
                    x_mid = x0 + i_date * self.width_day
                    x_start = x_mid - 0.5 * height_time_config
                    x_end = x_mid + 0.5 * height_time_config
                    
                    y1 = y_line_top - i_category * height_time_config
                    y2 = y1 - height_time_config
                    y_mid = 0.5 * (y1 + y2)
                    
                    # plot the diamond
                    x_list = [x_start, x_mid, x_end]
                    y1_list = [y_mid, y1, y_mid]
                    y2_list = [y_mid, y2, y_mid]
                    ax.fill_between(x_list, y1_list, y2_list, color=color, 
                                    lw=0.0, zorder=20_000)
            
                y_line_top = y_line_bottom

            else:
                raise ValueError(
                    f"Invalid type of task_config: {task_config.task_type}")
        
        #######################################################################
        # 5. plot the grid lines
        
        # 5.1. plot the grid lines from the top caption
        y_bottom = y_line_bottom
        
        x_start_top_caption = x0
        
        for i_data, data_dict in enumerate(top_caption_list):
            days = data_dict['days']
            
            width_month = self.width_day * days
            
            x_end_top_caption = x_start_top_caption + width_month
            
            # plot thick lines and caption 1
            if(self.key_top_caption == "year" and self.key_sub_caption == "month"  # noqa: E501
               or i_data == 0):
                ax.plot([x_start_top_caption, x_start_top_caption], 
                        [y_top, y_bottom], color='k', linewidth=lw_bold)
    
            else:
                ax.plot([x_start_top_caption, x_start_top_caption], 
                        [y_top, y_line2], color='k', linewidth=lw_bold)
                ax.plot([x_start_top_caption, x_start_top_caption], 
                        [y_line3, y_bottom], color='k', linewidth=lw_bold)
            
            x_start_top_caption = x_end_top_caption

        ax.plot([x_start_top_caption, x_start_top_caption], 
                [y_top, y_bottom], color='k', linewidth=lw_bold)

        # 5.2. plot the grid lines from the top sub caption
        x_start_sub_caption = x0
        
        for data_dict in sub_caption_list:
            days = data_dict['days']
            
            width_week = self.width_day * days
            
            x_end_sub_caption = x_start_sub_caption + width_week
            
            ax.plot([x_start_sub_caption, x_start_sub_caption], 
                    [y_line2, y_bottom], color='k', linewidth=lw_fine)
            ax.plot([x_end_week_caption, x_end_week_caption], 
                    [y_line2, y_bottom], color='k', linewidth=lw_fine)
            
            x_start_sub_caption = x_end_sub_caption
        
        #######################################################################
        # 6. print line of today
        if(self.today is not None):
            i_day = i_date_dict.get(
                self.today.strftime("%Y%m%d"), [None, None])[1]
            
            if(i_day is not None):
                x_tmp = x0 + i_day * self.width_day
                ax.plot([x_tmp, x_tmp], [y_line3, y_bottom], '-', color='r', 
                        linewidth=lw_fine, zorder=25_000)
        
        #######################################################################
        # 7. print further grid lines
        ax.plot([x_left, x_left], [y_top, y_bottom], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        ax.plot([x_left, x_right], [y_top, y_top], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        ax.plot([x_left, x_right], [y_line1, y_line1], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        ax.plot([x_left, x_right], [y_line2, y_line2], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        ax.plot([x_left, x_right], [y_line3, y_line3], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        ax.plot([x_left, x_right], [y_bottom, y_bottom], '-', color='k', 
                linewidth=lw_bold, zorder=10_000)
        
        #######################################################################
        # 8. print legend
        
        xlim = [x_left - 0.25, x_right + 0.25]
       
        legend_box_width = self.fs_legend / 72 * self.fac_inch_to_dim
        y_bottom = y_bottom - 0.5
    
        for key in self.category_dict:
            displayname = self.category_dict[key].displayname
            color = self.category_dict[key].color
            
            x = xlim[0] + 0.4 * (xlim[1] - xlim[0])
            
            x_list = [x, x + legend_box_width]
            y1_list = [y_bottom, y_bottom]
            y2_list = [y_bottom - legend_box_width, 
                       y_bottom - legend_box_width]
            
            ax.fill_between(x_list, y1_list, y2_list, color=color, lw=0.0)
            ax.text(x_list[1] + 0.5, y2_list[0] + 0.2,
                    displayname, fontsize=self.fs_legend)
            
            y_bottom = y_bottom - legend_box_width - 0.25
        
        ylim = [y_bottom - 0.25, y_top + 0.25]
        
        #######################################################################
        # 9. make figure great
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        ax.axis('off')
        
        #######################################################################
        # 10. resize image
        ax_w = (xlim[1] - xlim[0]) * self.fac_dim_to_inch
        ax_h = ax_w * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
        
        set_fig_size(fig, ax_w=ax_w, ax_h=ax_h, pad=pad)
        
        return fig



