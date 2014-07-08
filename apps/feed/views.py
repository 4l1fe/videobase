from django.shortcuts import render_to_response
from django.template import RequestContext

def some_view(request):
    # ...
    return render_to_response('my_template.html',
                              my_data_dictionary,
                              context_instance=RequestContext(request))