from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()

        context = {
            'form': form
            }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/register_success.html')
        
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form': form
        }

        return render(request, "accounts/login.html", context)

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)
            # Jehetu authenticationform use korchi, tai authenticate korte hobe na, sudhu get_user diye user ta niye nite hobe
            user = form.get_user()
            login(request, user)
            return redirect("home")
        
        context = {
            "form": form
        }
        return render(request, "accounts/login.html", context)
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")