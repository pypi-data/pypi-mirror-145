import datetime as dt
import plotly.express as px
import pytz

from django.contrib import admin
from django.shortcuts import redirect, render

from .models import Screenshot


def browse(request, time=None):
    screenshots = Screenshot.objects.order_by('-time')
    if time is None:
        screenshot = screenshots[:1][0]
        time = screenshot.time.isoformat()
        return redirect('browse-time', time=time)
    time = dt.datetime.fromisoformat(time)
    screenshots = screenshots.filter(time__lte=time)
    screenshot = screenshots[:1][0]
    if screenshot.time != time:
        time = screenshot.time.isoformat()
        return redirect('browse-time', time=time)
    context = {
        'screenshot': screenshot,
        **admin.site.each_context(request),
    }
    return render(request, 'emma/browse.html', context)


def browse_next(request, time):
    screenshots = Screenshot.objects.order_by('time')
    screenshot = screenshots.filter(time__gt=time)[:1][0]
    time = screenshot.time.isoformat()
    return redirect('browse-time', time=time)


def browse_prev(request, time):
    screenshots = Screenshot.objects.order_by('-time')
    screenshot = screenshots.filter(time__lt=time)[:1][0]
    time = screenshot.time.isoformat()
    return redirect('browse-time', time=time)


def histogram(request):
    times = Screenshot.objects.order_by('time').filter(display=0).values_list('time', flat=True)
    pacific = pytz.timezone('US/Pacific')
    times = [time.astimezone(pacific) for time in times]
    fig = px.histogram(times)
    fig.update_layout(
        title='Histogram of Screenshot Times',
        showlegend=False,
        xaxis_title='Time',
        yaxis_title='Count',
    )
    chart = fig.to_html(full_html=False)
    context = {
        'chart': chart,
        **admin.site.each_context(request),
    }
    return render(request, 'emma/histogram.html', context)
