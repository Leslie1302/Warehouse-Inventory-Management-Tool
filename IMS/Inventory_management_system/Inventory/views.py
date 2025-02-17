from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .forms import UserRegistration, AuthenticationForm, InventoryItemForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .models import InventoryItem, Category, Unit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from Inventory_management_system.settings import LOW_QUANTITY
from django.contrib import messages
# Create your views here.
class Index(TemplateView):
    template_name = 'Inventory/index.html'


LOW_QUANTITY = 10  # Example threshold

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Get user's groups
        user_groups = request.user.groups.all()

        # Filter items based on the groups the user belongs to
        items = InventoryItem.objects.filter(group__in=user_groups).order_by('id')

        # Find low inventory items in user's groups
        low_inventory = InventoryItem.objects.filter(
            group__in=user_groups,
            quantity__lte=LOW_QUANTITY
        )

        if low_inventory.exists():
            messages.error(
                request, 
                f"{low_inventory.count()} {'items have' if low_inventory.count() > 1 else 'item has'} low inventory"
            )

        low_inventory_ids = low_inventory.values_list('id', flat=True)

        return render(request, 'Inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})



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



class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'Inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'Inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'Inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'