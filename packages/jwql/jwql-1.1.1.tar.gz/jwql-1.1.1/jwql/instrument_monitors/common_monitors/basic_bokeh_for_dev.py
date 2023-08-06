from bokeh.plotting import figure, output_file, show



################################################
# Basic plot
# output to static HTML file
output_file("line.html")

p = figure(width=400, height=400)

# add a circle renderer with a size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

# show the results
show(p)
#################################################


from jwql.edb import engineering_database as ed
from datetime import datetime, timedelta
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout
from bokeh.models import BoxAnnotation
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import DatetimeTickFormatter

def add_limit_boxes(fig, yellow=None, red=None):
    """Add gree/yellow/red background colors
    """
    if yellow is not None:
        green = BoxAnnotation(bottom=yellow_limits[0], top=yellow_limits[1], fill_color='chartreuse', fill_alpha=0.2)
        fig.add_layout(green)
        if red is not None:
            yellow_high = BoxAnnotation(bottom=yellow_limits[1], top=red_limits[1], fill_color='gold', fill_alpha=0.2)
            fig.add_layout(yellow_high)
            yellow_low = BoxAnnotation(bottom=red_limits[0], top=yellow_limits[0], fill_color='gold', fill_alpha=0.2)
            fig.add_layout(yellow_low)
            red_high = BoxAnnotation(bottom=red_limits[1], top=red_limits[1]+100, fill_color='red', fill_alpha=0.1)
            fig.add_layout(red_high)
            red_low = BoxAnnotation(bottom=red_limits[0]-100, top=red_limits[0], fill_color='red', fill_alpha=0.1)
            fig.add_layout(red_low)
        else:
            yellow_high = BoxAnnotation(bottom=yellow_limits[1], top=yellow_limits[1] + 100, fill_color='gold', fill_alpha=0.2)
            fig.add_layout(yellow_high)
            yellow_low = BoxAnnotation(bottom=yellow_limits[0] - 100, top=yellow_limits[0], fill_color='gold', fill_alpha=0.2)
            fig.add_layout(yellow_low)
    else:
        if red is not None:
            green = BoxAnnotation(bottom=red_limits[0], top=red_limits[1], fill_color='chartreuse', fill_alpha=0.2)
            fig.add_layout(green)
            red_high = BoxAnnotation(bottom=red_limits[1], top=red_limits[1]+100, fill_color='red', fill_alpha=0.1)
            fig.add_layout(red_high)
            red_low = BoxAnnotation(bottom=red_limits[0]-100, top=red_limits[0], fill_color='red', fill_alpha=0.1)
            fig.add_layout(red_low)
    return fig

def add_dashed_line(fig, timevals, value):
    """Add a horizontal dashed line"""
    p.line(timevals, np.repeat(value, len(timevals)), line_dash='dashed')
    return p


times = np.array([datetime(2021,12,1,12,0,0) + timedelta(seconds=10 * n) for n in range(100)])
data = np.arange(len(times))
red_limits = [35, 85]
yellow_limits = [55, 65]

output_file("basic_telem.html")

p = figure(width=400, height=400, x_axis_label='Date', y_axis_label='Voltage',
          x_axis_type='datetime')
p.circle(times, data, size=4, color='navy', alpha=0.5)

nominal_value = 57.5
if nominal_value is not None:
    p = add_dashed_line(p, times, nominal_value)

p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %b %H:%M"],
        days=["%d %b %H:%M"],
        months=["%d %b %Y %H:%M"],
        years=["%d %b %Y"],
    )
p.xaxis.major_label_orientation = np.pi/4

p = add_limit_boxes(p, yellow=yellow_limits, red=red_limits)

show(p)
