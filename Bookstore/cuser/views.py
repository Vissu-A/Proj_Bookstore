from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from django.urls import reverse

from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.views.decorators.gzip import gzip_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.decorators.cache import never_cache, cache_control, cache_page

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth import authenticate, login, logout


from cuser import forms
from cuser.tasks import Account_Activate_Send_Mail
from cuser.models import User
from cuser.utils import token_generator
from cuser.forms import CustomUserInfoForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomSetPasswordForm
from .decorators import is_has_password

@require_http_methods(['POST', 'GET'])
def user_signup(request):

    if request.user.is_authenticated:
        return redirect('home-page')
    
    else:
        if request.method == 'POST':
            form = forms.CustomUserRegistrationForm(request.POST)

            if form.is_bound:
                if form.is_valid():

                    emailid = form.cleaned_data['email']
                    passcode = form.cleaned_data['password1']
                    fullname = form.cleaned_data['full_name'].capitalize()
                    phoneno = form.cleaned_data['phone']

                    user = User.objects.create_user(emailid, passcode, fullname)
                    user.is_active = False
                    user.phone = phoneno
                    user.save()

                    token = token_generator.make_token(user)
                    # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                    # get domain
                    domain = get_current_site(request).domain
                    print('###############################################')
                    print('domain is: ', domain)
                    print('###############################################')

                    # construct activation link with uidb64, token
                    link = reverse('activate-account-path', kwargs={'uidb64': uidb64, 'token': token})

                    activation_link = 'http://'+domain+link
                    print('###############################################')
                    print('Activation link is: ', activation_link)
                    print('###############################################')

                    task =  Account_Activate_Send_Mail.delay(emailid, fullname, activation_link)
                    print('Task ID is: ',task.task_id)

                    form = forms.CustomUserRegistrationForm()
                  
                    messages.success(request, 'User created successfully')
                    return redirect('user-created-path')
        
        else:
            form = forms.CustomUserRegistrationForm()

        return render(request, 'cuser/signup.html', {'form':form})


def user_signup_success(request):
    return render(request, 'cuser/user_created.html')



def activate_account(request, uidb64, token):

    uid = force_text(urlsafe_base64_decode(uidb64))
    print('#######################################')
    print('user id is: ', uid)
    print('#######################################')
    user = get_object_or_404(User, id=uid)

    if not token_generator.check_token(user, token):
        messages.error(request, 'Invalid Token. please check your activation link once.')
        return redirect('password_reset_confirm', uidb64=uidb64, token=token)

    elif user.is_active:
        messages.info(request, 'Account already activated, please login')
        return redirect('user-signin-path')

    else:
        user.is_active = True
        user.email_verified = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('user-signin-path')


def user_signin(request):

    if request.user.is_authenticated:
        return redirect('home-page')
    
    else:

        if request.method == 'POST':
            form = forms.Loginform(request.POST)
        
            email = request.POST['email']
            passcode = request.POST.get('passcode')
        
            if email and passcode:
            
                if not User.objects.filter(email=email).exists():    # if we use get instead of filter it will give DoesNotExists exception if user not there in the database.
                    form.add_error('email', 'There is no user with this email')
                
                else:
                    user = User.objects.get(email=email)

                    if not user.is_active:
                        form.add_error('email', 'Please activate your account before you login. For activation link please check your mail.')
                
                    elif not check_password(passcode, user.password):
                        form.add_error('passcode', 'Invalid Passcode!')
                        
                    else:
                        user = authenticate(request=request, email=email, password=passcode)
                    
                        if user is not None:
                            login(request, user)
                            if request.POST.get('next'):
                                return redirect(request.POST.get('next'))    # 'next' is for redirecting to @login_required() specified url, if no next then redirects to 'books-list' after user logedin successfully.
                                # or
                                # return HttpResponseRedirect(request.POST.get('next'),'/accounts/loggedin')
                            else:
                                return redirect('home-page')
        else:
            form = forms.Loginform()
        
        return render(request, 'cuser/signin.html', {'form':form})


def user_signout(request):
    logout(request)
    messages.info(request, 'You have loged out successfully')
    return redirect('user-signin-path')


@require_http_methods(['GET'])
@login_required
@is_has_password
def user_info(request, email=None):
    edit = True

    if email == None:
        form = CustomUserInfoForm(instance=request.user)

    else:
        user = User.objects.get(email = email)
        form = CustomUserInfoForm(instance=user)
        if email != request.user.email:
            edit = False
            
    return render(request, 'cuser/userinfo.html', {'form': form, 'edit': edit})

@login_required
@is_has_password
def user_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        print('#############################################')
        print('form is: ', form)
        print('#############################################')
        print()
        print('##################################################')
        print('Files are: ', request.FILES)
        print('##################################################')
        if form.is_bound:
            if form.is_valid():
                print('##################################################')
                print('Images file is: ', form.cleaned_data['img'])
                print('##################################################')
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('user-info-path')
            else:
                return render(request, 'useredit.html', {'form': form})
    else:
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'cuser/useredit.html', {'form': form})

@login_required
@is_has_password
def user_settings(request):
    if request.method == 'GET':
        # userobj = User.objects.get(pk=request.user.id)
        return render(request, 'cuser/settings.html')

@login_required
def set_user_password(request):
    print('user is: ', request.user)
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, data=request.POST)
        if form.is_bound:
            if form.is_valid():
                form.save()
                messages.info(request, 'Password set successfully. For security reasons we logged you out, plaese login again.')
                return redirect('user-signin-path')
    else:
        form =  CustomSetPasswordForm(request.user)
        messages.error(request, 'You must set a password to access any resource. Please set your password.')
    return render(request, 'cuser/set_password.html', {'form':form})


@login_required
@is_has_password
def user_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_bound:
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed successfully.For security reasons we logged you out, plaese login again.')
                return redirect('user-signin-path')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'cuser/password_change.html', {'form':form})



def test_response(request):
    return HttpResponse('<h1>Hello World!</h1>')