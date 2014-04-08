# coding: utf-8
from .forms import UsersProfileEditForm, UserEditForm, UserPicsEditForm
from apps.users.models import UsersProfile, UsersPics
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from apps.users.forms import UserPicsEditForm



def profile_edit(request):

    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        
        form = UsersProfileEditForm(request.POST) #A form bound to the POST data
        
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            pass
        form3 = UserPicsEditForm(request.POST, request.FILES)    
        if form3.is_valid():
            try:
                m = UsersPics.objects.get(user=request.user)
            except UsersPics.DoesNotExist:
                m= UsersPics(user = request.user)
                
            
            m.url = form3.cleaned_data['url']
            m.save()
            return HttpResponseRedirect('/profile/') # Redirect after POST
            
    else:
        
        up = UsersProfile.objects.get(user=request.user)
        upic = UsersProfile.objects.get(user=request.user)
        form = UsersProfileEditForm(instance=up)
        form2 = UserEditForm(instance=request.user)
        form3 = UserPicsEditForm(instance = upic)

    c = {
        'form':form ,
        'form2':form2,
        'form3':form3,
    }
    c.update(csrf(request))    
    #return HttpResponseRedirect('/admin/')
    return render_to_response( 'profile.html', c)