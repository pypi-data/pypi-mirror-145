# import os
import numpy as np
import pandas as pd
from math import pi

from bokeh.models.annotations import Title
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, curdoc
from bokeh.models import (CustomJS,
                          ColumnDataSource,
                          HoverTool,
                          CrosshairTool,
                          Span)
from bokeh.layouts import gridplot, layout
from bokeh.transform import factor_cmap, cumsum
from bokeh.palettes import Category20c

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`
    import importlib_resources as pkg_resources
from . import data as pkgdata


class AutoPlot:
    """Automated trading chart generator.
    
    Methods
    -------
    configure()
        Configure the plot settings.
    add_tool(tool_name)
        Add bokeh tool to plot. This adds the tool_name string to the fig_tools
        attribute.
    plot()
        Creates a trading chart of OHLC price data and indicators.
    
    """
    
    def __init__(self, data: pd.DataFrame):
        """Instantiates AutoPlot.

        Parameters
        ----------
        data : pd.DataFrame
            The OHLC price data to be charted. 

        Returns
        -------
        None
            AutoPlot will be instantiated and ready for plotting.

        """
        self._chart_theme = "caliber"
        self._max_indis_over = 3
        self._max_indis_below = 2
        self._modified_data = None
        self._fig_tools = "pan,wheel_zoom,box_zoom,undo,redo,reset,save,crosshair"
        self._ohlc_height = 400
        self._ohlc_width = 800
        self._top_fig_height = 150
        self._bottom_fig_height = 150
        self._jupyter_notebook = False
        self._show_cancelled = True
        self._use_strat_plot_data = False
        
        # Modify data index
        self._data = self._reindex_data(data)
        self._backtest_data = None
        
        # Load JavaScript code for auto-scaling 
        self._autoscale_code = pkg_resources.read_text(pkgdata, 'autoscale.js')
        
        
    def add_tool(self, tool_name: str) -> None:
        """Adds a tool to the plot. 

        Parameters
        ----------
        tool_name : str
            The name of tool to add (see Bokeh documentation).

        Returns
        -------
        None
            The tool will be added to the chart produced.
        
        """
        
        self._fig_tools = self._fig_tools + "," + tool_name
    
    
    def configure(self, max_indis_over: int = None, max_indis_below: int = None, 
                  fig_tools: str = None, ohlc_height: int = None, 
                  ohlc_width: int = None, top_fig_height: int = None, 
                  bottom_fig_height: int = None, jupyter_notebook: bool = None, 
                  show_cancelled: bool = None, chart_theme: str = None,
                  use_strat_plot_data: bool = False) -> None:
        """Configures the plot settings.

        Parameters
        ----------
        max_indis_over : int, optional
            Maximum number of indicators overlaid on the main chart. The 
            default is 3.
        max_indis_below : int, optional
            Maximum number of indicators below the main chart. The default is 2.
        fig_tools : str, optional
            The figure tools. The default is "pan,wheel_zoom,box_zoom,undo,
            redo,reset,save,crosshair".
        ohlc_height : int, optional
            The height (px) of the main chart. The default is 400.
        ohlc_width : int, optional
            The width (px) of the main chart. The default is 800.
        top_fig_height : int, optional
            The height (px) of the figure above the main chart. The default is 150.
        bottom_fig_height : int, optional
            The height (px) of the figure(s) below the main chart. The default is 150.
        jupyter_notebook : bool, optional
            Boolean flag when running in Jupyter Notebooks, to allow inline
            plotting. The default is False.
        show_cancelled : bool, optional
            Show/hide cancelled trades. The default is True.
        chart_theme : bool, optional
            The theme of the Bokeh chart generated. The default is "caliber".

        Returns
        -------
        None
            The plot settings will be saved to the active AutoTrader instance.
        
        """
        self._max_indis_over = max_indis_over if max_indis_over is not None else self._max_indis_over
        self._max_indis_below = max_indis_below if max_indis_below is not None else self._max_indis_below
        self._fig_tools = fig_tools if fig_tools is not None else self._fig_tools
        self._ohlc_height = ohlc_height if ohlc_height is not None else self._ohlc_height
        self._ohlc_width = ohlc_width if ohlc_width is not None else self._ohlc_width
        self._top_fig_height = top_fig_height if top_fig_height is not None else self._top_fig_height
        self._bottom_fig_height = bottom_fig_height if bottom_fig_height is not None else self._bottom_fig_height
        self._jupyter_notebook = jupyter_notebook if jupyter_notebook is not None else jupyter_notebook
        self._show_cancelled = show_cancelled if show_cancelled is not None else self._show_cancelled
        self._chart_theme = chart_theme if chart_theme is not None else self._chart_theme
        self._use_strat_plot_data = use_strat_plot_data if use_strat_plot_data is not None else self._use_strat_plot_data
        
    
    def plot(self, instrument: str = None, indicators: dict = None, 
             backtest_dict: dict = None, cumulative_PL: list = None,
             show_fig: bool = True) -> None:
        """Creates a trading chart of OHLC price data and indicators.

        Extended Summary
        ----------------
        The following lists the keys corresponding to various indicators,
        which can be included in the chart using the indicators argument.
        
        over : over
            Generic line indicator over chart with key: data
        below : below
            Generic line indicator below chart with key: data
        MACD : below
            MACD indicator with keys: macd, signal, histogram
        MA : over
             Moving average overlay indicator with key: data
        RSI : below
            RSI indicator with key: data
        STOCHASTIC : below
            Stochastics indicator with keys: K, D
        Heikin-Ashi : below
            Heikin Ashi candlesticks with key: data
        Supertrend : over
            Supertrend indicator with key: data
        Swings : over
            Swing levels indicator with key: data
        Engulfing : below
            Engulfing candlestick pattern with key: data
        Crossover : below
            Crossover indicator with key: data
        Grid : over
            Grid levels with key: data
        Pivot : over
            Pivot points with keys: data
        HalfTrend : over
            Halftrend indicator with key: data
        multi : below
            Multiple indicator type 
        signals : over
            Trading signals plot with key: data 
        bands : over
            Shaded bands indicator type 
        threshold : below
            Threshold indicator type 
        trading-session : over
            Highlighted trading session times with key: data
        
        Parameters
        ----------
        instrument : str, optional
            The traded instrument name. The default is None.
        backtest_dict : dict, optional
            The backtest results dictionary. The default is None.
        indicators : dict, optional
            Indicators dictionary. The default is None.
        cumulative_PL : list, optional
            Cumulative PL history. The default is None.
        show_fig : bool, optional
            Flag to show the chart. The default is True.

        Returns
        -------
        None
            Calling this method will automatically generate and open a chart.
        
        See Also
        --------
        autotrader.autotrader.AutoTrader.analyse_backtest
        """
        
        # Preparation
        if backtest_dict is None:
            # Using Indiview
            if instrument is not None:
                title_string = "AutoTrader IndiView - {}".format(instrument)
            else:
                title_string = "AutoTrader IndiView"
            output_file("indiview-chart.html", title = title_string)
            
        else:
            # Plotting backtest results
            if instrument is None:
                instrument = backtest_dict['instrument']
            title_string = f"Backtest chart for {instrument} ({backtest_dict['interval']} candles)"
            output_file(f"{instrument}-backtest-chart.html",
                        title=f"AutoTrader Backtest Results - {instrument}")
        
        # Add base data
        source = ColumnDataSource(self._data)
        
        # Main plot
        if self._use_strat_plot_data:
            source.add(np.ones(len(self._data))*max(self._data.plot_data), 'High')
            source.add(np.ones(len(self._data))*min(self._data.plot_data), 'Low')
            main_plot = self._create_main_plot(source)
        else:
            source.add((self._data.Close >= self._data.Open).values.astype(np.uint8).astype(str),
                       'change')
            main_plot = self._plot_candles(source)
        
        top_figs = []
        bottom_figs = []
        
        if backtest_dict is not None:
            account_hist = backtest_dict['account_history']
            if len(account_hist) != len(self._data):
                account_hist = self._interpolate_and_merge(account_hist)
            NAV = account_hist['NAV']
            balance = account_hist['balance']
            trade_summary = backtest_dict['trade_summary']
            indicators = backtest_dict['indicators']
            open_trades = backtest_dict['open_trades']
            cancelled_trades = backtest_dict['cancelled_trades']
            
            # Top plots
            top_fig = self._plot_line(NAV, main_plot, new_fig=True, 
                                      legend_label='Net Asset Value', 
                                      hover_name='NAV')
            self._plot_line(balance, top_fig, legend_label='Account Balance', 
                            hover_name='P/L', line_colour='blue')
            top_figs.append(top_fig)
            
            if not self._use_strat_plot_data:
                # Overlay trades
                # TODO - add way to visualise trades without candles
                self._plot_trade_history(trade_summary, main_plot)
                if len(cancelled_trades) > 0 and self._show_cancelled:
                    self._plot_trade_history(cancelled_trades, main_plot, cancelled_summary=True)
                if len(open_trades) > 0:
                    self._plot_trade_history(open_trades, main_plot, open_summary=True)
        
        # Indicators
        if indicators is not None:
            bottom_figs = self._plot_indicators(indicators, main_plot)
        
        # Auto-scale y-axis of candlestick chart
        # TODO - also autoscale indicators
        autoscale_args = dict(y_range = main_plot.y_range, source = source)
        main_plot.x_range.js_on_change('end', CustomJS(args = autoscale_args, 
                                       code = self._autoscale_code))
        
        # Compile plots for final figure
        plots = top_figs + [main_plot] + bottom_figs
        linked_crosshair = CrosshairTool(dimensions='both')
        
        titled = 0
        t = Title()
        t.text = title_string
        for plot in plots:
            if plot is not None:
                plot.xaxis.major_label_overrides = {
                    i: date.strftime('%b %d %Y') for i, date in enumerate(pd.to_datetime(self._data["date"]))
                }
                plot.xaxis.bounds = (0, self._data.index[-1])
                plot.sizing_mode = 'stretch_width'
                
                if titled == 0:
                    plot.title = t
                    titled = 1
                
                if plot.legend:
                    plot.legend.visible = True
                    plot.legend.location = 'top_left'
                    plot.legend.border_line_width = 1
                    plot.legend.border_line_color = '#333333'
                    plot.legend.padding = 5
                    plot.legend.spacing = 0
                    plot.legend.margin = 0
                    plot.legend.label_text_font_size = '8pt'
                    plot.legend.click_policy = "hide"
                
                plot.add_tools(linked_crosshair)
                plot.min_border_left = 0
                plot.min_border_top = 3
                plot.min_border_bottom = 6
                plot.min_border_right = 10
                plot.outline_line_color = 'black'
    
        # Construct final figure
        fig = gridplot(plots, ncols = 1, toolbar_location = 'right',
                       toolbar_options = dict(logo = None), 
                       merge_tools = True)
        fig.sizing_mode = 'stretch_width'
        
        # Set theme - # TODO - adapt line colours based on theme
        curdoc().theme = self._chart_theme
        
        if show_fig:
            if self._jupyter_notebook:
                output_notebook()
            show(fig)
        
    
    def _reindex_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Resets index of data to obtain integer indexing.
        """
        if isinstance(data, pd.Series):
            modified_data = data.to_frame(name='plot_data')
        else:
             modified_data = data.copy()
        modified_data['date'] = modified_data.index
        modified_data = modified_data.reset_index(drop = True)
        modified_data['data_index'] = modified_data.index
        return modified_data
    
    
    def _resample_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Resamples data to match the time index of the base data.
        """
        return data.reindex(self._data.date, method='ffill')
    
    
    def _check_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Checks the length of the inputted data against the base data, 
        and resamples it if necessary.
        """
        if len(data) != len(self._data):
            data = self._resample_data(data)
        return data
        
    
    def _merge_data(self, data: pd.DataFrame, name=None) -> pd.DataFrame:
        """Merges the provided data with the base data, using the data of the 
        base data and the index of the data to be merged.
        
        Parameters:
            data: the data to be merged
            name: the desired column name of the merged data
        """
        # TODO - need to add handling of different data types, ie. list vs. series vs. df
        # Mainly check if the series has a name or not
        merged_data = pd.merge(self._data, data, left_on='date', 
                               right_index=True).fillna('')
        
        if name is not None:
            merged_data.rename(columns={data.name: name}, inplace=True)
        
        return merged_data
    
    
    def _interpolate_and_merge(self, df):
        dt_data = self._data.set_index('date')
        concat_data = pd.concat([dt_data, df]).sort_index()
        concat_data.index = pd.to_datetime(concat_data.index, utc=True)
        interp_data = concat_data.interpolate(method='nearest').fillna(method='bfill')
        merged_data = self._merge_data(interp_data).drop_duplicates()
        merged_data = merged_data.replace('', np.nan).fillna(method='ffill')
        return merged_data[list(df.columns) + ['date']].set_index('date')
    
    
    def _add_backtest_price_data(self, backtest_price_data: pd.DataFrame) -> None:
        """Processes backtest price data to included integer index of base 
        data.
        """
        temp_data = self._data.copy()
        temp_data.index = temp_data['date']
        
        self._backtest_data = temp_data.reindex(backtest_price_data.index, method='ffill')
    
    
    ''' ------------------- FIGURE MANAGEMENT METHODS --------------------- '''
    def _plot_multibot_backtest(self, multibot_backtest_results: dict, 
                                NAV: pd.Series, cpl_dict: pd.Series,
                                margin_available: pd.Series):
        """Creates multi-bot backtest figure. 
        
            Parameters:
                multibot_backtest_results (df): dataframe of bot backtest results.
                
                NAV (list): Net asset value.
                
                cpl_dict (dict): cumulative PL of each bot.
        """
        
        # TODO - merge this into self.plot method?
        # First, clean up individual plots (pie, etc) into new methods
        
        # Preparation
        output_file("candlestick.html",
                    title = "AutoTrader Multi-Bot Backtest Results")
        
        linked_crosshair = CrosshairTool(dimensions='both')
        if len(multibot_backtest_results) < 3:
            multibot_backtest_results['color'] = Category20c[3][0:len(multibot_backtest_results)]
        else:
            multibot_backtest_results['color'] = Category20c[len(multibot_backtest_results)]
            
        MBR = ColumnDataSource(multibot_backtest_results)
        
        # Account Balance 
        navfig = figure(plot_width = self._ohlc_width,
                        plot_height = self._top_fig_height,
                        title = None,
                        active_drag = 'pan',
                        active_scroll = 'wheel_zoom')
        
        # Add glyphs
        navfig.line(self._data.index, 
                    NAV, 
                    line_color = 'black',
                    legend_label = 'Backtest Net Asset Value')
        
        navfig.xaxis.major_label_overrides = {
                    i: date.strftime('%b %d %Y') for i, date in enumerate(pd.to_datetime(self._data["date"]))
                }
        navfig.xaxis.bounds = (0, self._data.index[-1])
        navfig.sizing_mode = 'stretch_width'
        navfig.legend.location = 'top_left'
        navfig.legend.border_line_width   = 1
        navfig.legend.border_line_color   = '#333333'
        navfig.legend.padding             = 5
        navfig.legend.spacing             = 0
        navfig.legend.margin              = 0
        navfig.legend.label_text_font_size = '8pt'
        navfig.add_tools(linked_crosshair)
        
        # Win rate bar chart
        instruments = multibot_backtest_results.index.values
        
        winrate = self._plot_bars(instruments, 'win_rate', MBR, 
                                  fig_title='Bot win rate (%)',
                                  hover_name='win_rate%')
        
        winrate.sizing_mode = 'stretch_width'
        
        
        # Pie chart of trades per bot
        pie_data = pd.Series(multibot_backtest_results.no_trades).reset_index(name='value').rename(columns={'index':'instrument'})
        pie_data['angle'] = pie_data['value']/pie_data['value'].sum() * 2*pi
        if len(multibot_backtest_results) < 3:
            pie_data['color'] = Category20c[3][0:len(multibot_backtest_results)]
        else:
            pie_data['color'] = Category20c[len(multibot_backtest_results)]

        pie = self._plot_pie(pie_data, fig_title="Trade distribution")
        
        pie.axis.axis_label=None
        pie.axis.visible=False
        pie.grid.grid_line_color = None
        pie.sizing_mode = 'stretch_width'
        pie.legend.location = "top_left"
        pie.legend.border_line_width = 1
        pie.legend.border_line_color = '#333333'
        pie.legend.padding = 5
        pie.legend.spacing = 0
        pie.legend.margin = 0
        pie.legend.label_text_font_size = '8pt'
        
        # Bar plot for avg/max win/loss
        win_metrics = ['Average Win', 'Max. Win']
        lose_metrics = ['Average Loss', 'Max. Loss']
        
        abs_max_loss = -1.2*max(multibot_backtest_results.max_loss)
        abs_max_win = 1.2*max(multibot_backtest_results.max_win)
        
        pldata = {'instruments': instruments,
                'Average Win': multibot_backtest_results.avg_win.values,
                'Max. Win': multibot_backtest_results.max_win.values - 
                            multibot_backtest_results.avg_win.values,
                'Average Loss': -multibot_backtest_results.avg_loss.values,
                'Max. Loss': multibot_backtest_results.avg_loss.values - 
                             multibot_backtest_results.max_loss.values}
        
        TOOLTIPS = [
                    ("Instrument:", "@instruments"),
                    ("Max win", "@{Max. Win}"),
                    ("Avg. win", "@{Average Win}"),
                    ("Max Loss", "@{Max. Loss}"),
                    ("Avg. loss", "@{Average Loss}"),
                    ]
        
        plbars = figure(x_range=instruments,
                        y_range=(abs_max_loss, abs_max_win),
                        title="Win/Loss breakdown",
                        toolbar_location=None,
                        tools = "hover",
                        tooltips = TOOLTIPS,
                        plot_height = 250)

        plbars.vbar_stack(win_metrics,
                     x='instruments',
                     width = 0.9,
                     color = ('#008000', '#FFFFFF'),
                     line_color='black',
                     source = ColumnDataSource(pldata),
                     legend_label = ["%s" % x for x in win_metrics])

        plbars.vbar_stack(lose_metrics,
                     x = 'instruments',
                     width = 0.9,
                     color = ('#ff0000' , '#FFFFFF'),
                     line_color='black',
                     source = ColumnDataSource(pldata),
                     legend_label = ["%s" % x for x in lose_metrics])
        
        plbars.x_range.range_padding = 0.1
        plbars.ygrid.grid_line_color = None
        plbars.legend.location = "bottom_center"
        plbars.legend.border_line_width   = 1
        plbars.legend.border_line_color   = '#333333'
        plbars.legend.padding             = 5
        plbars.legend.spacing             = 0
        plbars.legend.margin              = 0
        plbars.legend.label_text_font_size = '8pt'
        plbars.axis.minor_tick_line_color = None
        plbars.outline_line_color = None
        plbars.sizing_mode = 'stretch_width'
    
        # Cumulative PL
        cplfig = figure(plot_width = navfig.plot_width,
                        plot_height = self._top_fig_height,
                        title = None,
                        active_drag = 'pan',
                        active_scroll = 'wheel_zoom',
                        x_range = navfig.x_range)
        
        # self._data['data_index'] = self._data.reset_index(drop=True).index
        
        if len(multibot_backtest_results) < 3:
            colors = Category20c[3][0:len(multibot_backtest_results)]
        else:
            colors = Category20c[len(multibot_backtest_results)]
        
        for ix, instrument in enumerate(cpl_dict):
            cpldata = cpl_dict[instrument].copy().to_frame()
            cpldata['date'] = cpldata.index
            cpldata = cpldata.reset_index(drop = True)
            
            cpldata = pd.merge(self._data, cpldata, left_on='date', right_on='date')
            
            cplfig.line(cpldata.data_index.values,
                        cpldata.profit.values,
                        legend_label = "{}".format(instrument),
                        line_color = colors[ix])
        
        cplfig.legend.location = 'top_left'
        cplfig.legend.border_line_width = 1
        cplfig.legend.border_line_color = '#333333'
        cplfig.legend.padding = 5
        cplfig.legend.spacing = 0
        cplfig.legend.margin = 0
        cplfig.legend.label_text_font_size = '8pt'
        cplfig.sizing_mode = 'stretch_width'
        cplfig.add_tools(linked_crosshair)
        
        cplfig.xaxis.major_label_overrides = {
                    i: date.strftime('%b %d %Y') for i, date in enumerate(pd.to_datetime(self._data["date"]))
                }
        cplfig.xaxis.bounds = (0, self._data.index[-1])
        
        # Margin Available 
        marfig = figure(plot_width = self._ohlc_width,
                        plot_height = self._top_fig_height,
                        title = None,
                        active_drag = 'pan',
                        active_scroll = 'wheel_zoom',
                        x_range = navfig.x_range)
        
        # Add glyphs
        marfig.line(self._data.index, 
                    margin_available, 
                    line_color = 'black',
                    legend_label = 'Margin Available')
        
        marfig.xaxis.major_label_overrides = {
                    i: date.strftime('%b %d %Y') for i, date in enumerate(pd.to_datetime(self._data["date"]))
                }
        marfig.xaxis.bounds = (0, self._data.index[-1])
        marfig.sizing_mode = 'stretch_width'
        marfig.legend.location = 'top_left'
        marfig.legend.border_line_width = 1
        marfig.legend.border_line_color = '#333333'
        marfig.legend.padding = 5
        marfig.legend.spacing = 0
        marfig.legend.margin = 0
        marfig.legend.label_text_font_size = '8pt'
        marfig.add_tools(linked_crosshair)
        
        # Construct final figure     
        final_fig = layout([  
                                   [navfig],
                            [winrate, pie, plbars],
                                   [cplfig],
                                   [marfig]
                            ])
        final_fig.sizing_mode = 'scale_width'
        
        # Set theme - # TODO - adapt line colours based on theme
        curdoc().theme = self._chart_theme
        
        if self._jupyter_notebook:
            output_notebook()
        show(final_fig)
    
        
    def _plot_indicators(self, indicators: dict, linked_fig):
        """Plots indicators based on indicator type. If inidcator type is 
        "over", it will be plotted on top of linked_fig. If indicator type is 
        "below", it will be plotted on a new figure below the OHLC chart.
        """
        # TODO - convert all data to a ColumnDataSource, to allow indicator
        # autoscaling and proper index matching. Create helper method for this
        
        x_range   = self._data.index
        plot_type = {'MACD'        : 'below',
                     'MA'          : 'over',
                     'RSI'         : 'below',
                     'STOCHASTIC'  : 'below',
                     'Heikin-Ashi' : 'below',
                     'Supertrend'  : 'over',
                     'Swings'      : 'over',
                     'Engulfing'   : 'below',
                     'Crossover'   : 'below',
                     'over'        : 'over',
                     'below'       : 'below',
                     'Grid'        : 'over',
                     'Pivot'       : 'over',
                     'HalfTrend'   : 'over',
                     'multi'       : 'below',
                     'signals'     : 'over',
                     'bands'       : 'over',
                     'threshold'   : 'below',
                     'trading-session': 'over'}
        
        # Plot indicators
        indis_over = 0
        indis_below = 0
        bottom_figs = []
        colours = ['red', 'blue', 'orange', 'green', 'black', 'yellow']
        
        for indicator in indicators:
            indi_type = indicators[indicator]['type']
            
            if indi_type in plot_type:
                # The indicator plot type is recognised
                if plot_type[indi_type] == 'over' and \
                    indis_over < self._max_indis_over and \
                        not self._use_strat_plot_data:
                    if indi_type == 'Supertrend':
                        self._plot_supertrend(indicators[indicator]['data'], 
                                              linked_fig)
                        indis_over     += 1 # Count as 2 indicators
                    elif indi_type == 'HalfTrend':
                        self._plot_halftrend(indicators[indicator]['data'], 
                                             linked_fig)
                        indis_over     += 1 # Count as 2 indicators
                    elif indi_type == 'Swings':
                        self._plot_swings(indicators[indicator]['data'], 
                                          linked_fig)
                    elif indi_type == 'Grid':
                        self._plot_grid(indicators[indicator]['data'], 
                                        linked_fig)
                    elif indi_type == 'Pivot':
                        self._plot_pivot_points(indicators[indicator], 
                                                linked_fig)
                    elif indi_type == 'signals':
                        self._plot_signals(linked_fig, 
                                           indicators[indicator]['data'])
                        
                    elif indi_type == 'bands':
                        self._plot_bands(indicators[indicator], 
                                         linked_fig=linked_fig, new_fig=False,
                                         legend_label=indicator)
                    
                    elif indi_type == 'trading-session':
                        self._plot_trading_session(indicators[indicator],
                                                   linked_fig)
                    
                    else:
                        # Generic overlay indicator - plot as line
                        if type(indicators[indicator]['data']) == pd.Series:
                            # Merge indexes
                            merged_indicator_data = pd.merge(self._data, 
                                                             indicators[indicator]['data'], 
                                                             left_on='date', 
                                                             right_index=True)
                            line_data = merged_indicator_data[indicators[indicator]['data'].name]
                            x_vals = line_data.index
                            y_vals = line_data.values
                        else:
                            x_vals = x_range
                            y_vals = indicators[indicator]['data']
                        
                        linked_fig.line(x_vals, y_vals, line_width = 1.5, 
                                        legend_label = indicator,
                                        line_color = indicators[indicator]['color'] if 'color' in indicators[indicator] else colours[indis_over])
                    indis_over += 1
                    
                elif plot_type[indi_type] == 'below' and indis_below < self._max_indis_below:
                    if indi_type == 'MACD':
                        new_fig = self._plot_macd(x_range, indicators[indicator], 
                                                  linked_fig)
                        new_fig.title = indicator
                    
                    elif indi_type == 'Heikin-Ashi':
                        
                        HA_data = self._reindex_data(indicators[indicator]['data'])
                        source = ColumnDataSource(HA_data)
                        source.add((HA_data.Close >= HA_data.Open).values.astype(np.uint8).astype(str),
                                   'change')
                        new_fig = self._plot_candles(source)
                        new_fig.x_range = linked_fig.x_range
                        new_fig.y_range = linked_fig.y_range
                        new_fig.title = indicator
                        indis_below += self._max_indis_below # To block any other new plots below.
                    
                    elif indi_type == 'RSI':
                        new_fig = self._plot_line(indicators[indicator]['data'], linked_fig,
                                        legend_label=indicator, new_fig=True)
                        if 'swings' in indicators[indicator]:
                            self._plot_swings(indicators[indicator]['swings'], 
                                              new_fig)
                            
                    elif indi_type == 'multi':
                        # Plot multiple lines on the same figure
                        new_fig = figure(plot_width = linked_fig.plot_width,
                                         plot_height = 130,
                                         title = indicator,
                                         tools = linked_fig.tools,
                                         active_drag = linked_fig.tools[0],
                                         active_scroll = linked_fig.tools[1],
                                         x_range = linked_fig.x_range)
                        
                        for dataset in list(indicators[indicator].keys())[1:]:
                            if type(indicators[indicator][dataset]['data']) == pd.Series:
                                # Merge indexes
                                merged_indicator_data = pd.merge(self._data, 
                                                                 indicators[indicator][dataset]['data'], 
                                                                 left_on='date', 
                                                                 right_index=True)
                                line_data = merged_indicator_data[indicators[indicator][dataset]['data'].name]
                                x_vals = line_data.index
                                y_vals = line_data.values
                            else:
                                x_vals = x_range
                                y_vals = indicators[indicator][dataset]['data']
                            
                            new_fig.line(x_vals, y_vals,
                                         line_color = indicators[indicator][dataset]['color'] if \
                                             'color' in indicators[indicator][dataset] else 'black', 
                                         legend_label = dataset)
                    
                    elif indi_type == 'threshold':
                        new_fig = self._plot_bands(indicators[indicator], 
                                         linked_fig=linked_fig, legend_label=indicator)
                    
                    else:
                        # Generic indicator - plot as line
                        if isinstance(indicators[indicator]['data'], pd.Series):
                            # Timeseries provided, merge indexes
                            if indicators[indicator]['data'].name is None:
                                indicators[indicator]['data'].name = 'data'
                            merged_indicator_data = pd.merge(self._data, 
                                                             indicators[indicator]['data'], 
                                                             left_on='date', 
                                                             right_index=True)
                            line_data = merged_indicator_data[indicators[indicator]['data'].name]
                            x_vals = line_data.index
                            y_vals = line_data.values
                        else:
                            # List provided
                            x_vals = x_range
                            y_vals = np.zeros(len(x_range))
                            y_vals[:len(indicators[indicator]['data'])] = indicators[indicator]['data']
                            
                        new_fig = figure(plot_width = linked_fig.plot_width,
                                         plot_height = 130,
                                         title = None,
                                         tools = linked_fig.tools,
                                         active_drag = linked_fig.tools[0],
                                         active_scroll = linked_fig.tools[1],
                                         x_range = linked_fig.x_range)
                        
                        # Add glyphs
                        new_fig.line(x_vals, y_vals,
                                     line_color = indicators[indicator]['color'] if \
                                         'color' in indicators[indicator] else 'black', 
                                     legend_label = indicator)
                        
                    indis_below += 1
                    bottom_figs.append(new_fig)
            else:
                # The indicator plot type is not recognised - plotting on new fig
                if indis_below < self._max_indis_below:
                    print("Indicator type '{}' not recognised in AutoPlot.".format(indi_type))
                    new_fig = self._plot_line(indicators[indicator]['data'], 
                                              linked_fig, new_fig=True, 
                                              legend_label=indicator, 
                                              hover_name=indicator)
                    
                    indis_below += 1
                    bottom_figs.append(new_fig)
                
        return bottom_figs
    
    
    def _create_main_plot(self, source, line_colour: str = 'black',
                          legend_label: str = 'Data'):
        fig = figure(plot_width = self._ohlc_width,
                     plot_height = 150,
                     title = "Custom Plot Data",
                     tools = self._fig_tools,
                     active_drag = 'pan',
                     active_scroll = 'wheel_zoom',)
        
        fig.line('data_index', 'plot_data', 
                 line_color = line_colour,
                 # legend_label = legend_label,
                 source = source)
        
        return fig
    
    
    def _plot_line(self, plot_data, linked_fig, new_fig=False, fig_height=150,
                   fig_title=None, legend_label=None, hover_name=None,
                   line_colour='black'):
        """Generic method to plot data as a line.
        """
        
        # Initiate figure
        if new_fig:
            fig = figure(plot_width = linked_fig.plot_width,
                         plot_height = fig_height,
                         title = fig_title,
                         tools = self._fig_tools,
                         active_drag = 'pan',
                         active_scroll = 'wheel_zoom',
                         x_range = linked_fig.x_range)
        else:
            fig = linked_fig
        
        # Add glyphs
        if len(plot_data) != len(self._data):
            # Mismatched timeframe
            merged_data = self._merge_data(plot_data, name='plot_data')
            source = ColumnDataSource(merged_data)
        else:
            source = ColumnDataSource(self._data)
            source.add(plot_data, 'plot_data')
        
        fig.line('data_index', 'plot_data', 
                 line_color = line_colour,
                 legend_label = legend_label,
                 source = source)
        
        if hover_name is not None:
            fig_hovertool = HoverTool(tooltips = [("Date", "@date{%b %d %H:%M}"),
                                                  (hover_name, "@{plot_data}{%0.2f}")
                                                  ], 
                                      formatters={'@{plot_data}' : 'printf',
                                                  '@date' : 'datetime'},
                                      mode = 'vline')
            
            fig.add_tools(fig_hovertool)
        
        return fig
    
    
    ''' ------------------------ OVERLAY PLOTTING ------------------------- '''
    def _plot_candles(self, source):
        ''' Plots OHLC data onto new figure. '''
        bull_colour             = "#D5E1DD"
        bear_colour             = "#F2583E"
        candle_colours          = [bear_colour, bull_colour]
        colour_map              = factor_cmap('change', candle_colours, ['0', '1'])
        
        candle_tooltips         = [("Date", "@date{%b %d %H:%M:%S}"),
                                   ("Open", "@Open{0.0000}"), 
                                   ("High", "@High{0.0000}"), 
                                   ("Low", "@Low{0.0000}"),
                                   ("Close", "@Close{0.0000}")]
    
        candle_plot = figure(plot_width     = self._ohlc_width, 
                             plot_height    = self._ohlc_height, 
                             tools          = self._fig_tools,
                             active_drag    = 'pan',
                             active_scroll  = 'wheel_zoom')
    
        candle_plot.segment('index', 'High',
                            'index', 'Low', 
                            color   = "black",
                            source  = source)
        candles = candle_plot.vbar('index', 0.7, 'Open', 'Close', 
                                   source       = source,
                                   line_color   = "black", 
                                   fill_color   = colour_map)
        
        candle_hovertool = HoverTool(tooltips   = candle_tooltips, 
                                  formatters    = {'@date':'datetime'}, 
                                  mode          = 'vline',
                                  renderers     = [candles])
        
        candle_plot.add_tools(candle_hovertool)
        
        return candle_plot
    
    
    def _plot_swings(self, swings, linked_fig):
        '''
        Plots swing detection indicator.
        '''
        swings = pd.merge(self._data, swings, left_on='date', right_index=True).fillna('')
        
        linked_fig.scatter(list(swings.index),
                            list(swings.Last.values),
                            marker = 'dash',
                            size = 15,
                            fill_color = 'black',
                            legend_label = 'Last Swing Price Level')
    
    
    def _plot_supertrend(self, st_data, linked_fig):
        """Plots supertrend indicator.
        """
        # Extract supertrend data
        # uptrend     = st_data['uptrend']
        # dntrend     = st_data['downtrend']
        
        # reset index 
        st_data['date']         = st_data.index 
        st_data                 = st_data.reset_index(drop = True)
        
        # Add glyphs
        linked_fig.scatter(st_data.index,
                    st_data['uptrend'],
                    size = 5,
                    fill_color = 'blue',
                    legend_label = 'Up trend support')
        linked_fig.scatter(st_data.index,
                    st_data['downtrend'],
                    size = 5,
                    fill_color = 'red',
                    legend_label = 'Down trend support')
    
    
    def _plot_halftrend(self, htdf, linked_fig):
        ''' Plots halftrend indicator. '''
        # reset index 
        htdf['date'] = htdf.index 
        htdf = htdf.reset_index(drop = True)
        long_arrows = htdf[htdf.buy != 0]
        short_arrows = htdf[htdf.sell != 0]
        
        # Add glyphs
        linked_fig.scatter(htdf.index,
                           htdf['atrLow'],
                           size = 3,
                           fill_color = 'blue',
                           legend_label = 'ATR Support')
        linked_fig.scatter(htdf.index,
                           htdf['atrHigh'],
                           size = 3,
                           fill_color = 'red',
                           legend_label = 'ATR Resistance')
        linked_fig.line(htdf.index,
                           htdf['atrLow'],
                           line_color = 'blue')
        linked_fig.line(htdf.index,
                           htdf['atrHigh'],
                           line_color = 'red')
        
        # Add buy and sell entry signals
        self._plot_trade(long_arrows.index, long_arrows.atrLow, 
                         'triangle', 'green', 'Buy Signals', linked_fig, 10)
        self._plot_trade(short_arrows.index, short_arrows.atrHigh, 
                         'inverted_triangle', 'red', 'Sell Signals', 
                         linked_fig, 10)
    
    
    def _plot_signals(self, linked_fig, signals_df):
        """Plots long and short entry signals over OHLC chart.
        """
        
        signals_df = signals_df.reset_index(drop = True)
        long_arrows = signals_df[signals_df['buy'] != 0]
        short_arrows = signals_df[signals_df['sell'] != 0]
        
        # Add buy and sell entry signals
        self._plot_trade(long_arrows.index, long_arrows.buy, 
                         'triangle', 'lightgreen', 'Buy Signals', linked_fig, 12)
        self._plot_trade(short_arrows.index, short_arrows.sell, 
                         'inverted_triangle', 'orangered', 'Sell Signals', 
                         linked_fig, 12)
    
    
    def _plot_grid(self, grid_levels, linked_fig, linewidth=0.5):
        for price in grid_levels:
            hline = Span(location=price, 
                         dimension='width',
                         line_color='black',
                         line_dash='dashed',
                         line_width=linewidth)
            linked_fig.add_layout(hline)
    
    
    def _plot_pivot_points(self, pivot_dict, linked_fig, levels=1):
        """Adds pivot points to OHLC chart.
        """
        pivot_df = pivot_dict['data']
        levels = pivot_dict['levels'] if 'levels' in pivot_dict else levels
        
        # Check pivot_df 
        pivot_df = self._check_data(pivot_df)
        
        # Merge to integer index
        pivot_df = pd.merge(self._data, pivot_df, left_on='date', right_index=True)
        
        # Remove NaNs
        pivot_df = pivot_df.fillna('')
        
        linked_fig.scatter(list(pivot_df.index),
                           list(pivot_df['pivot'].values),
                           marker = 'dash',
                           size = 15,
                           line_color = 'black',
                           legend_label = 'Pivot')
        
        if levels > 0:        
            linked_fig.scatter(list(pivot_df.index),
                               list(pivot_df['s1'].values),
                               marker = 'dash',
                               size = 15,
                               line_color = 'blue',
                               legend_label = 'Support 1')
            
            linked_fig.scatter(list(pivot_df.index),
                               list(pivot_df['r1'].values),
                               marker = 'dash',
                               size = 15,
                               line_color = 'red',
                               legend_label = 'Resistance 1')
            
            if levels > 1:
                linked_fig.scatter(list(pivot_df.index),
                                   list(pivot_df['s2'].values),
                                   marker = 'dot',
                                   size = 10,
                                   line_color = 'blue',
                                   legend_label = 'Support 2')
                
                linked_fig.scatter(list(pivot_df.index),
                                   list(pivot_df['r2'].values),
                                   marker = 'dot',
                                   size = 10,
                                   line_color = 'red',
                                   legend_label = 'Resistance 2')
                
                if levels > 2:
                    linked_fig.scatter(list(pivot_df.index),
                                       list(pivot_df['s3'].values),
                                       marker = 'dot',
                                       size = 7,
                                       line_color = 'blue',
                                       legend_label = 'Support 3')
                    
                    linked_fig.scatter(list(pivot_df.index),
                                       list(pivot_df['r3'].values),
                                       marker = 'dot',
                                       size = 7,
                                       line_color = 'red',
                                       legend_label = 'Resistance 3')
        
        
    def _plot_trading_session(self, session_plot_data, linked_fig):
        """Shades trading session times.
        """
        
        session = session_plot_data['data'].lower()
        fill_color = session_plot_data['fill_color'] if 'fill_color' in session_plot_data else 'blue'
        fill_alpha = session_plot_data['fill_alpha'] if 'fill_alpha' in session_plot_data else 0.3
        line_color = session_plot_data['line_color'] if 'line_color' in session_plot_data else None
        
        times = {'sydney': {'start': '21:00', 'end': '05:00'},
                 'london': {'start': '08:00', 'end': '16:00'},
                 'new york': {'start': '13:00', 'end': '21:00'},
                 'tokyo': {'start': '23:00', 'end': '07:00'},
                 'frankfurt': {'start': '07:00', 'end': '15:00'}
                 }
        
        index_data = self._data.set_index('date')
        
        midpoint = max(self._data.High.values)
        height = 2*midpoint
        
        session_start = times[session]['start']
        session_end = times[session]['end']
        
        session_data = index_data.between_time(session_start, session_end)
        
        opens = session_data[session_data.data_index - session_data.data_index.shift(1) != 1].data_index
        closes = session_data[(session_data.data_index - session_data.data_index.shift(1) != 1).shift(-1).fillna(True)].data_index
        
        linked_fig.hbar(midpoint, height, opens, closes, 
                        line_color = line_color, 
                        fill_color = fill_color,
                        fill_alpha = fill_alpha,
                        legend_label = f'{session} trading session')
        
        
    ''' ----------------------- TOP FIG PLOTTING -------------------------- '''
    def _plot_trade(self, x_data, y_data, marker_type, marker_colour, 
                    label, linked_fig, scatter_size=15):
        """Plots individual trade.
        """
        
        linked_fig.scatter(x_data, y_data,
                           marker       = marker_type,
                           size         = scatter_size,
                           fill_color   = marker_colour,
                           legend_label = label)
    
    
    def _plot_trade_history(self, trade_summary, linked_fig, 
                            cancelled_summary=False, open_summary=False):
        """Plots trades taken over ohlc chart.
        """
        
        exit_summary = trade_summary.copy()
        
        if self._backtest_data is not None:
            # Charting on different timeframe data
            trade_summary = pd.merge(self._backtest_data, trade_summary, 
                                     left_index=True, right_index=True)
        else:
            trade_summary = pd.merge(self._data, trade_summary, 
                                     left_on='date', right_index=True)
        
        # Backtesting signals
        long_trades = trade_summary[trade_summary['direction'] > 0]
        shorts_trades = trade_summary[trade_summary['direction'] < 0]
        
        if cancelled_summary is False and open_summary is False:
            
            if self._backtest_data is not None:
                # Charting on different timeframe data
                exit_summary = pd.merge(self._backtest_data, exit_summary, 
                                        left_index=True, right_on='exit_time')
            else:
                exit_summary = pd.merge(self._data, exit_summary, 
                                        left_on='date', right_on='exit_time')
            
            profitable_longs = long_trades[(long_trades['profit'] > 0)]
            unprofitable_longs = long_trades[(long_trades['profit'] < 0)]
            profitable_shorts = shorts_trades[(shorts_trades['profit'] > 0)]
            unprofitable_shorts = shorts_trades[(shorts_trades['profit'] < 0)]
            
            # Profitable long trades
            if len(profitable_longs) > 0:
                self._plot_trade(list(profitable_longs.data_index.values),
                                 list(profitable_longs.fill_price.values), 
                                 'triangle', 'lightgreen', 
                                 'Profitable long trades', linked_fig)
    
            # Profitable short trades
            if len(profitable_shorts) > 0:
                self._plot_trade(list(profitable_shorts.data_index.values),
                                 list(profitable_shorts.fill_price.values),
                                 'inverted_triangle', 'lightgreen',
                                 'Profitable short trades', linked_fig)
            
            # Unprofitable long trades
            if len(unprofitable_longs) > 0:
                self._plot_trade(list(unprofitable_longs.data_index.values),
                                 list(unprofitable_longs.fill_price.values),
                                 'triangle', 'orangered',
                                 'Unprofitable long trades', linked_fig)
            
            # Unprofitable short trades
            if len(unprofitable_shorts) > 0:
                self._plot_trade(list(unprofitable_shorts.data_index.values),
                                 list(unprofitable_shorts.fill_price.values),
                                 'inverted_triangle', 'orangered',
                                 'Unprofitable short trades', linked_fig)
        else:
            if cancelled_summary:
                long_legend_label = 'Cancelled long trades'
                short_legend_label = 'Cancelled short trades'
                fill_color = 'black'
                price = 'order_price'
            else:
                long_legend_label = 'Open long trades'
                short_legend_label = 'Open short trades'
                fill_color = 'white'
                price = 'fill_price'
        
            # Partial long trades
            if len(long_trades) > 0:
                linked_fig.scatter(list(long_trades.data_index.values),
                                   list(long_trades[price].values),
                                   marker = 'triangle',
                                   size = 15,
                                   fill_color = fill_color,
                                   legend_label = long_legend_label)
            
            # Partial short trades
            if len(shorts_trades) > 0:
                linked_fig.scatter(list(shorts_trades.data_index.values),
                                   list(shorts_trades[price].values),
                                   marker = 'inverted_triangle',
                                   size = 15,
                                   fill_color = fill_color,
                                   legend_label = short_legend_label)
        
        
        # Stop loss  levels
        if None not in trade_summary.stop_loss.values:
            self._plot_trade(list(trade_summary.data_index.values),
                             list(trade_summary.stop_loss.fillna('').values),
                             'dash', 'black', 'Stop loss', linked_fig)
        
        # Take profit levels
        if None not in trade_summary.take_profit.values:
            self._plot_trade(list(trade_summary.data_index.values),
                             list(trade_summary.take_profit.fillna('').values),
                             'dash', 'black', 'Take profit', linked_fig)
        
        # Position exits
        if cancelled_summary is False and open_summary is False:
            self._plot_trade(list(exit_summary.data_index),
                             list(exit_summary.exit_price.values),
                             'circle', 'black', 'Position exit', linked_fig,
                             scatter_size=7)
    
    
    ''' --------------------- BOTTOM FIG PLOTTING ------------------------- '''
    def _plot_macd(self, x_range, macd_data, linked_fig):
        """Plots MACD indicator.
        """
        # Initialise figure
        fig = figure(plot_width = linked_fig.plot_width,
                     plot_height = self._bottom_fig_height,
                     title = None,
                     tools = linked_fig.tools,
                     active_drag = linked_fig.tools[0],
                     active_scroll = linked_fig.tools[1],
                     x_range = linked_fig.x_range)
        
        # Add glyphs
        source = ColumnDataSource(self._data)
        for key, item in macd_data.items():
            if key == 'type':
                pass
            else:
                merged_data = self._merge_data(item)[item.name]
                source.add(merged_data, key)
            
        fig.line('data_index', 'macd', source=source, line_color = 'blue')
        fig.line('data_index', 'signal', source=source, line_color = 'red')
        if 'histogram' in macd_data:
            histcolour = []
            for i in range(len(macd_data['histogram'])):
                if np.isnan(macd_data['histogram'][i]):
                    histcolour.append('lightblue')
                else:
                    if macd_data['histogram'][i] < 0:
                        histcolour.append('red')
                    else:
                        histcolour.append('lightblue')
                        
            fig.quad(top = macd_data['histogram'],
                     bottom = 0,
                     left = x_range - 0.3,
                     right = x_range + 0.3,
                     fill_color = histcolour)
            
        if 'crossvals' in macd_data:
            fig.scatter(x_range,
                        macd_data['crossvals'],
                        marker = 'dash',
                        size = 15,
                        fill_color = 'black',
                        legend_label = 'Last Crossover Value')
    
        return fig
    
    
    ''' -------------------- MISCELLANEOUS PLOTTING ----------------------- '''
    def _plot_bars(self, x_vals, data_name, source, linked_fig=None, fig_height=250,
                   fig_title=None, hover_name=None):
        fig = figure(x_range = x_vals,
                     title = fig_title,
                     toolbar_location = None,
                     tools = 'hover',
                     tooltips = "@index: @{}".format(hover_name),
                     plot_height = fig_height)
        
        fig.vbar(x = 'index', 
                 top = data_name,
                 width = 0.9,
                 color = 'color',
                 source = source)
        
        return fig
    
    
    def _plot_pie(self, source, fig_title=None, fig_height=250):
        
        pie = figure(title = fig_title, 
                     toolbar_location = None,
                     tools = "hover", 
                     tooltips="@instrument: @value",
                     x_range=(-1, 1),
                     y_range=(0.0, 2.0),
                     plot_height = fig_height)
        
        pie.wedge(x=0, y=1, radius=0.3,
                  start_angle=cumsum('angle', include_zero=True), 
                  end_angle=cumsum('angle'),
                  line_color="white", 
                  fill_color='color',
                  legend_field='instrument',
                  source=source)
        
        return pie
    
    
    def _plot_bands(self, plot_data, linked_fig=None, new_fig = True,
                    fill_color = 'blue', fill_alpha = 0.3, line_color='black',
                    legend_label = None):
        """Plots a shaded region bound by upper and lower vaues.
        
        lower, upper and mid data must have same length as self._data.
        
        Parameters: 
            plot_data (dict): a dictionary containing keys 'lower', 'upper', 
            corresponding to the lower and upper bounding values (which may be
            an integer or timeseries). Optional keys include:
                - band_name: legend name for bands
                - fill_color: color filling upper and lower bands
                - fill_alpha: transparency of fill (0 - 1)
                - mid: data for a mid line
                - mid_name: legend name for mid line
                - line_color: line color for mid line
            
            linked_fig (Bokeh figure): linked figure
            
            new_fig (bool): flag to return a new figure or overlay on linked_fig
        """
        
        fill_color = plot_data['fill_color'] if 'fill_color' in plot_data else fill_color
        fill_alpha = plot_data['fill_alpha'] if 'fill_alpha' in plot_data else fill_alpha
        line_color = plot_data['line_color'] if 'line_color' in plot_data else line_color
        
        if new_fig:
            # Plot on new fig
            fig = figure(plot_width     = linked_fig.plot_width,
                         plot_height    = self._bottom_fig_height,
                         title          = None,
                         tools          = linked_fig.tools,
                         active_drag    = linked_fig.tools[0],
                         active_scroll  = linked_fig.tools[1],
                         x_range        = linked_fig.x_range)
            
        else:
            # Plot over linked figure
            fig = linked_fig
        
        # Charting on different timeframe data
        lower_band = self._merge_data(plot_data['lower'], name='lower')['lower']
        upper_band = self._merge_data(plot_data['upper'], name='upper')['upper']
        
        fig.varea(lower_band.index, 
                  lower_band.values, 
                  upper_band.values,
                  fill_alpha = fill_alpha, 
                  fill_color = fill_color,
                  legend_label = plot_data['band_name'] if 'band_name' in plot_data else legend_label)
        
        if 'mid' in plot_data:
            # Add a mid line
            mid_line = self._merge_data(plot_data['mid'], name='mid')['mid']
            fig.line(mid_line.index, mid_line.values, line_color=line_color,
            legend_label = plot_data['mid_name'] if 'mid_name' in plot_data else 'Band Mid Line')
        
        return fig
    