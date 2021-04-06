from .models import User
from django.shortcuts import redirect
from django.contrib import messages

def is_has_password(func):
    def wrapper(request, *args, **kwargs):
        print('inside wrapper function')
        print('function is: ', func)
        print('request is: ', request)
        print('user is ', request.user)
        print(request.user.has_usable_password())
        if request.user.has_usable_password():
            return func(request, *args, **kwargs)
        else:
            return redirect('set-user-password')
    return wrapper