from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from .forms import UserRegistration, AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LogoutView as BaseLogoutView
# Create your views here.
class Index(TemplateView):
    template_name = 'Inventory/index.html'


class Dashboard(View):
    def get(self, request):
        return render(request, 'Inventory/dashboard.html')


class SignUpView(View):
    def get(self, request):
        form = UserRegistration()
        return render(request, 'Inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegistration(request.POST)

        if form.is_valid():
            form.save()
            User = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, User)
            return redirect('index')

        return render(request, 'Inventory/signup.html', {'form': form})



class SignInView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'Inventory/signin.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)  # Pass POST data to the form

        if form.is_valid():
            user = form.get_user()  # Authenticate the user
            login(request, user)
            return redirect('index')

        return render(request, 'Inventory/signin.html', {'form': form})

    
class CustomLogoutView(BaseLogoutView):
    http_method_names = ['get', 'post']  # Allow both GET and POST requests
