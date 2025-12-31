from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect("home")
    
class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)

        context = {
            'form': form
        }
        
        return render(request, "accounts/profile.html", context)
    
    def post(self, request):
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        
        context = {
            'form': form
        }

        return render(request, "accounts/profile.html", context)
    
class CustomPasswordChangeView( LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been changed successfully.")
        return response
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
