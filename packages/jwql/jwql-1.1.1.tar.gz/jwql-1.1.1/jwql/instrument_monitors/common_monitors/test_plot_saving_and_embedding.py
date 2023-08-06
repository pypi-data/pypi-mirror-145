#! /usr/bin/env python

"""Test out the stragegy of saving a bokeh plot to a file and then reading it in and
embedding it in a webpage
"""
from copy import deepcopy
from bokeh.embed import json_item
from bokeh.plotting import figure
import json
import numpy as np
from datetime import datetime
from bokeh.embed import components, json_item
from bokeh.layouts import gridplot
from bokeh.models import BoxAnnotation, ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, output_file, show, save
from bokeh.models.widgets import Tabs, Panel


x = [datetime(2021,10,i) for i in range(3, 8)]
y = [1,2,3,4,5]
source = ColumnDataSource(data={'x': x, 'y': y})
fig = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST', x_axis_label='Time',
                     y_axis_label='Hours')
data = fig.scatter(x='x', y='y', line_width=1, line_color='blue', source=source)

# Make the x axis tick labels look nice
fig.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig.xaxis.major_label_orientation = np.pi/4
hover_tool = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data])
hover_tool.formatters={'@x': 'datetime'}
fig.tools.append(hover_tool)


item_text = json.dumps(json_item(fig, "myplot"))
print(item_text)
with open('fig_data.json', 'w') as outfile:
    outfile.write(item_text)





x2 = deepcopy(x)
y2 = [1,2,3,4,5]
source2 = ColumnDataSource(data={'x': x2, 'y': y2})

fig2 = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST2', x_axis_label='Time',
                     y_axis_label='Hours')
data2 = fig2.scatter('x', 'y', line_width=1, line_color='blue', source=source2)

# Make the x axis tick labels look nice
fig2.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig2.xaxis.major_label_orientation = np.pi/4

hover_tool2 = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data2])
hover_tool2.formatters={'@x': 'datetime'}
fig2.tools.append(hover_tool2)


item_text = json.dumps(json_item(fig2, "myplot"))
print(item_text)
with open('fig2_data.json', 'w') as outfile:
    outfile.write(item_text)




x3 = deepcopy(x)
y3 = [1,2,3,4,5]
source3 = ColumnDataSource(data={'x': x3, 'y': y3})

fig3 = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST3', x_axis_label='Time',
                     y_axis_label='Hours')
data3 = fig3.scatter('x', 'y',  line_width=1, line_color='blue', source=source3)

# Make the x axis tick labels look nice
fig3.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig3.xaxis.major_label_orientation = np.pi/4

hover_tool3 = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data3])
hover_tool3.formatters={'@x': 'datetime'}
fig3.tools.append(hover_tool3)







"""WORKS
fig = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST', x_axis_label='Time',
                     y_axis_label='Hours')
x = [datetime(2021,10,i) for i in range(3, 8)]
y = [4,5,6]
source = ColumnDataSource(data={'x': x, 'y': y})
data = fig.scatter(x='x',y='y', line_width=1, line_color='blue', source=source)
fig.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig.xaxis.major_label_orientation = np.pi/4
hover_tool = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data])
hover_tool.formatters={'@x': 'datetime'}
fig.tools.append(hover_tool)



fig2 = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST', x_axis_label='Time',
                     y_axis_label='Hours')
source2 = ColumnDataSource(data={'x': x, 'y': y})
data2 = fig2.scatter(x='x',y='y', line_width=1, line_color='blue', source=source2)
fig2.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig2.xaxis.major_label_orientation = np.pi/4
hover_tool2 = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data2])
hover_tool2.formatters={'@x': 'datetime'}
fig2.tools.append(hover_tool2)


fig3 = figure(tools='pan,box_zoom,reset,wheel_zoom,save', x_axis_type='datetime',
                     title='TEST', x_axis_label='Time',
                     y_axis_label='Hours')
source3 = ColumnDataSource(data={'x': x, 'y': y})
data3 = fig3.scatter(x='x',y='y', line_width=1, line_color='blue', source=source3)
fig3.xaxis.formatter=DatetimeTickFormatter(
                    hours=["%d %b %H:%M"],
                    days=["%d %b %H:%M"],
                    months=["%d %b %Y %H:%M"],
                    years=["%d %b %Y"]
                )
fig3.xaxis.major_label_orientation = np.pi/4
hover_tool3 = HoverTool(tooltips=[('Value', '@y'),
                                         ('Date', '@x{%d %b %Y %H:%M:%S}')
                                        ], mode='mouse', renderers=[data3])
hover_tool3.formatters={'@x': 'datetime'}

fig3.tools.append(hover_tool3)
"""



#grid = gridplot([[fig, fig2], [None, fig3]], width=250, height=250)
grid = gridplot([fig, fig2, fig3], ncols=2)  # merge_tools=False --> gives tool buttons for each plot
#show(grid)

grid2 = gridplot([fig3, fig, fig2], ncols=1)

# Create two panels, one for each conference
power_panel = Panel(child=grid, title='Eastern Conference')
voltage_panel = Panel(child=grid2, title='Western Conference')

# Assign the panels to Tabs
tabs = Tabs(tabs=[power_panel, voltage_panel])

# Show the tabbed layout
show(tabs)




item_text = json.dumps(json_item(tabs, "myplot"))
#print(item_text)

with open('tabbed_plots.json', 'w') as outfile:
    outfile.write(item_text)