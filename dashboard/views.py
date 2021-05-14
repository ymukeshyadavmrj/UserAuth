from django.shortcuts import render
from dashboard.forms import UserForm,UserProfileInfoForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login , logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'dashboard/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("you are logged in !")


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            #if 'profile_pics' in request.FILES:
            #    profile.profile_pic = request.FILES['profile_pics']

            profile.save()

            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'dashboard/registration.html',{'user_form':user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered})


def user_login(request):

    if request.method == "POST":
        username1 = request.POST.get('username')
        password1= request.POST.get('password')

        user = authenticate(username=username1,password=password1)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active!")

        else:
            # print("someone tried to login and failed!")
            # print("username: {} and password: {}".format(username1,password1))
            return HttpResponse("Invalid login details supplied for {}".format(username1))
    else:
        return render(request,'dashboard/login.html')
