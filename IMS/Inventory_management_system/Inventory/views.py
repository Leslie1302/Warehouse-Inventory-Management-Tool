from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .forms import UserRegistration, AuthenticationForm, InventoryItemForm, InventoryItemFormSet
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .models import InventoryItem, Category, Unit
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from Inventory_management_system.settings import LOW_QUANTITY
from django.contrib import messages
# Create your views here.
class Index(TemplateView):
    template_name = 'Inventory/index.html'


LOW_QUANTITY = 5  # Set threshold

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Inventory.view_inventoryitem'

    def get(self, request):
        user = request.user

        # ✅ Admins see everything
        if user.is_superuser:
            items = InventoryItem.objects.all()
        else:
            # ✅ Users see only items based on their group
            items = InventoryItem.objects.filter(group__in=user.groups.all())

        # ✅ Identify low stock items
        low_inventory_items = items.filter(quantity__lte=LOW_QUANTITY)  
        low_inventory_ids = list(low_inventory_items.values_list('id', flat=True))  
        low_inventory_names = list(low_inventory_items.values_list('name', flat=True))  

        return render(request, 'Inventory/dashboard.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids,
            'low_inventory_items': low_inventory_names  # ✅ Send names for the alert
        })


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



class AddItem(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Inventory.add_inventoryitem'
    template_name = 'Inventory/item_form.html'

    def get(self, request):
        formset = InventoryItemFormSet()
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        formset = InventoryItemFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    item = form.save(commit=False)
                    item.user = request.user  # Assign the user who created the item

                    # Assign to the first group the user belongs to (if any)
                    if request.user.groups.exists():
                        item.group = request.user.groups.first()

                    item.save()
            return redirect(reverse_lazy('dashboard'))
        return render(request, self.template_name, {'formset': formset})



class EditItem(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'Inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    permission_required = 'Inventory.change_inventoryitem'

class DeleteItem(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'Inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'

    permission_required = 'Inventory.delete_inventoryitem'

