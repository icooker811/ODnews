from django.shortcuts import render,redirect
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from accounts.forms import UserloginForm

def LoginView(request):
    if request.method == 'POST':
        form = UserloginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                 login(request, user)
                 if request.GET.get('next'): 
                    return redirect( request.GET['next'] )
                 else : 
                    return redirect( 'news:index' )
            else:
                return render(request, 'login.html', {
                    'form' : form,
                    'error_message': "The password is valid, but the account has been disabled!",
                })
        else:
            return render(request, 'login.html', {
                'form' : form,
                'error_message': "The username and password were incorrect.",
            })
    form = UserloginForm()
    return render(request, 'login.html', {'form' : form})


def logoutView(request):
    logout(request)
    return redirect(('news:index'))