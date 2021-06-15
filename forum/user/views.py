from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from user.forms import LoginUser, UserForm
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.contrib.auth.decorators import  login_required
from django.views import View

# Create your views here.
# def profile(request):
#     if request.method == "POST":
#         profile_form = UserForm(request.POST, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, ('Your profile was successfully updated!'))
#         else:
#             messages.error(request, 'Unable to update data')
#         return redirect('user.html')
#     user_profile = UserForm(instance=request.user)
#     return render(request, 'user.html', {"user":request.user,"user_profile":user_profile})


def login(request):
    if not request.user.is_anonymous:
        return redirect(reverse("home"))
    context = {"login_form": LoginUser()}
    if request.method == "POST":
        login_form = LoginUser(request.POST)
        if login_form.is_valid():
            password = login_form.cleaned_data['password']
            username = login_form.cleaned_data['username']
            user = authenticate(username = username, password = password)
            if user.is_active:
                log_in(request, user)
            return redirect(reverse('home'))
        else:
            context["login_form"] = login_form
    return render(request, 'login_page.html', context)

@login_required(login_url="login")
def logout(request):
    log_out(request)
    return redirect(reverse("home"))

class Registration(View):
    form_class = UserForm
    template_name = 'signup.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.context.update(registration_form = self.form_class())
            return render(request, self.template_name, self.context)
        else:
            return redirect(reverse('home'))
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        self.context.update(registration_form = form)
        return render(request, self.template_name, self.context)