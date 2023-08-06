# -*- coding: utf-8 -*-
"""
Module containing utility functions.
"""


def set_fig_size(fig, fig_w=None, ax_w=None, fig_h=None, ax_h=None, 
                 pad=1.08, gs=None, h_pad=None, w_pad=None, 
                 max_it=10, tol=1e-4):
    """
    Sets the size of a figure. This method allows to set both the
    figure width/heigth or axis width/height. If the ax-width or ax-height
    is set, then the figure size is determined iteratively, so that the
    desired ax size is set.

    See :func:`set_fig_size`, which should be used when the figure consists
    of a grid of subplots and each subplot should have the same size.
    
    .. note::
        If the size of the axis is set, then the size of the first axis
        will be tracked. This method works best, if only one axis is
        available.
    
    .. note::
        For this method, exactly one parameter of ``fig_w`` and ``ax_w`` and
        exactly one parameter of ``fig_h`` and ``ax_h`` must be set.
    
    Parameters
    ----------
    fig : Figure
        Matplotlib figure of which to adjust the size.
        
    fig_w : float
        Width of the figure, optional. Either ``fig_w`` or ``ax_w`` must be
        set.
        
    ax_w : float
        Width of the axis, optional. Either ``fig_w`` or ``ax_w`` must be
        set.
        
    fig_h : float
        Width of the figure, optional. Either ``fig_h`` or ``ax_h`` must be
        set.
        
    ax_h : float
        Width of the axis, optional. Either ``fig_h`` or ``ax_h`` must be
        set.
    
    pad : float
        Parameter to determine the whitespace around the axis.
        
    gs : GridSpec
        Used GridSpec for the subplots. If provided, then the ``tight_layout``
        method will be called on ``gs``, utilizing the ``h_pad``
        and ``w_pad`` parameters. If not provided, then the ``tight_layout``
        will be called on the provided figure ``fig``.
        
    h_pad : float
        Horizontal spacing. Only used, if ``gs`` is provided.
        
    w_pad : float
        Vertical spacing. Only used, if ``gs`` is provided.
        
    max_it : int
        Maximum number of iterations.
        
    tol : float
        Allowed tolerance for defined ax width or ax height. Allows for
        faster termination of the iteration.
        
    
    Examples
    --------
    
    .. code-block:: python
        
        import numpy as np
        import matplotlib.pyplot as plt
        
        from TFAFramework.plot_util import set_fig_size, activate_latex_tud
        
        activate_latex_tud()
        
        # 1. create test data
        X = np.linspace(0, 10, 50)
        y = X**2
        
        # 2. plot data
        fig = plt.figure()
        ax = fig.gca()
        
        ax.plot(X, y)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        
        # 3. perform set_fig_size method
        
        # following combinations are possible
        
        # a) fig_w and fig_h (equivalent to calling fig.set_figwidth() 
        # and fig.set_figheight)
        set_fig_size(fig, fig_w=4, fig_h=3, pad=0.1)
    
        # b) ax_w and fig_h
        set_fig_size(fig, ax_w=4, fig_h=3, pad=0.1)
    
        # c) fig_w and ax_h
        set_fig_size(fig, fig_w=4, ax_h=3, pad=0.1)
    
        # d) ax_w and ax_h
        set_fig_size(fig, ax_w=4, ax_h=3, pad=0.1)
        
    """
    
    # 1. perform checks
    if(fig_w is None and ax_w is None):
        raise ValueError(
            "Either fig_w or ax_w must be set, but both parameters are None.")
        
    if(fig_w is not None and ax_w is not None):
        raise ValueError(
            "Both fig_w and ax_w are set, but only one of those parameters"
            " can be set.")
        
    if(fig_h is None and ax_h is None):
        raise ValueError(
            "Either fig_h or ax_h must be set, but both parameters are None.")
        
    if(fig_h is not None and ax_h is not None):
        raise ValueError(
            "Both fig_h and ax_h are set, but only one of those parameters"
            " can be set.")
        
    # 2. set initial size
    if(fig_w is not None):
        fig_w_tmp = fig_w
    else:
        if(gs is None):
            fig_w_tmp = 1.25 * ax_w
        else:
            fig_w_tmp = 1.5 * gs.ncols * ax_w
        
    if(fig_h is not None):
        fig_h_tmp = fig_h
    else:
        if(gs is None):
            fig_h_tmp = 1.25 * ax_h
        else:
            fig_h_tmp = 1.5 * gs.nrows * ax_h
    
    # initial resize of the figure
    fig.set_figwidth(fig_w_tmp)
    fig.set_figheight(fig_h_tmp)
    
    if(gs is None):
        fig.tight_layout(pad=pad)
    else:
        gs.tight_layout(fig, pad=pad, h_pad=h_pad, w_pad=w_pad)
    
    # if fig_w and fig_h are provided: done
    if(fig_w is not None and fig_h is not None):
        return
    
    # 3. iteration to set size of the axis
    
    # don't use fig.gca(), since it might return the color bar
    ax = fig.get_axes()[0]
    
    for i in range(max_it):
        # 3.1. get size of axis in inches
        # source: https://stackoverflow.com/a/19306776 (Author: unutbu)
        bbox = ax.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted())
        ax_w_tmp, ax_h_tmp = bbox.width, bbox.height
        
        # 3.2. check, if size of axis is within tolerances
        b1 = True
        if(ax_w is not None and abs(ax_w_tmp - ax_w) > tol):
            b1 = False
            
        b2 = True
        if(ax_h is not None and abs(ax_h_tmp - ax_h) > tol):
            b2 = False
            
        if(b1 and b2):
            return
        
        # 3.3. get size of figure
        fig_w_tmp, fig_h_tmp = fig.get_size_inches()
        
        # 3.4. calculate margin = difference between figure size and axis size
        margin_w = fig_w_tmp - ax_w_tmp
        margin_h = fig_h_tmp - ax_h_tmp
        
        # 3.5. calculate new figure sizes
        if(ax_w is not None):
            fig_w_new = ax_w + margin_w
        else:
            fig_w_new = fig_w
            
        if(ax_h is not None):
            fig_h_new = ax_h + margin_h
        else:
            fig_h_new = fig_h
            
        # 3.6. resize figure
        fig.set_figwidth(fig_w_new)
        fig.set_figheight(fig_h_new)

        if(gs is None):
            fig.tight_layout(pad=pad)
        else:
            gs.tight_layout(fig, pad=pad, h_pad=h_pad, w_pad=w_pad)
            
            
def get_data_list(date_data_list, key, name_list=None):
    """
    Divides the given days into periods, where one value is constant
    (e.g. the month). For each period, the value itself (e.g. month index),
    the displayname, and the number of days in this period is determined.
    
    This function is needed to get the top caption and top sub caption.
    
    For example, if ``key`` is ``"month"``, then the months between
    the start date and the end date are determined. Furthermore, the
    displayname and the number of dates for each
    month is obtained for each month.
    
    
    Parameters
    ----------
    date_data_list : list
        List, which contains the required data (year, month, week, quarter) 
        for each day to consider.
        
    key : str
        Key to consider. Possible choises are ``"year"``, ``"month"``, 
        ``"week"``, and ``"quarter"``.
        
    name_list : list of str
        Displayname for each possible entry. If ``None``, then the
        respective string representation of the value (e.g. "2022" for the
        year 2022) is used.
    
    
    Returns
    -------
    data_list : list
        List of the data for each time period (e.g. month). Each entry 
        contains the value, displayname and number of days for this 
        time period. Following keys are used:
            
        +-------------------+-------------------+---------------------------+
        | Key               | Type              | Description               |
        +-------------------+-------------------+---------------------------+
        | ``value``         | different         | Current value (e.g. month |
        |                   |                   | index)                    |
        +-------------------+-------------------+---------------------------+
        | ``displayname``   | str               | String representation of  |
        |                   |                   | the value.                |
        +-------------------+-------------------+---------------------------+
        | ``day``           | int               | Number of days for the    |
        |                   |                   | given time period.        | 
        +-------------------+-------------------+---------------------------+
    """
    
    # 1. resulting list
    data_list = []
    
    # 2. get current value, set number of days to 0
    current_value = date_data_list[0][key]
    days = 0
    
    # 3. iterate over each day
    for i_dd, dd in enumerate(date_data_list):
        # 3.1. get current data
        val_tmp = dd[key]
        
        # 3.2. value has changed, save it
        if(current_value != val_tmp):
            # get displayname
            if(name_list is None):
                displayname = f"{current_value}"
            else:
                displayname = name_list[current_value]
            
            # save data
            data_list.append({
                'value': current_value,
                'displayname': displayname,
                'days': days
            })
        
            # update current values
            current_value = val_tmp
            days = 1
            
        else:
            # nothing has changed, increase number of days.
            days += 1
    
    # 4. add values for the last period
    if(name_list is None):
        displayname = f"{current_value}"
    else:
        displayname = name_list[current_value]

    data_list.append({
        'value': current_value,
        'displayname': displayname,
        'days': days
    })
    
    # 5. return data
    return data_list
    
    

