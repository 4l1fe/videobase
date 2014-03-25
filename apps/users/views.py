# coding: utf-8
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from itertools import groupby

from apps.users.logentry_summary import *

class FilterForm(forms.Form):
    start_at = forms.DateField(widget=SelectDateWidget(), label=u'с')
    end_at = forms.DateField(widget=SelectDateWidget(), label=u'по')

class LogentrySummaryView(TemplateView):
    template_name = 'admin/logentry_summary.html'

    def get_context_data(self, **kwargs):

        context = super( LogentrySummaryView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            filter_form = FilterForm(self.request.POST)
            end_at = filter_form['end_at']
            start_at = filter_form['start_at']
            report = LogentrySummary(period ={'start_at': start_at.value(), 'end_at': end_at.value()})
        else:
            end_at = datetime.now()
            start_at = (datetime.now() - timedelta(days = datetime.now().weekday()))
            report = LogentrySummary(period ={'start_at': start_at, 'end_at': end_at})
            filter_form = FilterForm(initial={ 'end_at': end_at, 'start_at': start_at})


        context['report_data'] = report.summary()
        context['filter_form'] = filter_form.as_table()

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)
