# Inventory/urls.py
from django.urls import path
from .views import (
    Index, SignUpView, SignInView, CustomLogoutView, Dashboard, AddItem, 
    EditItem, DeleteItem, RequestMaterialView, MaterialOrdersView, 
    UpdateMaterialStatusView, ProfileView
)

urlpatterns = [
    # Public routes
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', CustomLogoutView.as_view(template_name='Inventory/logout.html'), name='logout'),
    
    # Authenticated routes
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item', AddItem.as_view(), name='add-item'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('request-material/', RequestMaterialView.as_view(), name='request_material'),
    path('material-orders/', MaterialOrdersView.as_view(), name='material_orders'),
    
    # Parameterized routes
     path('update_material_status/<int:order_id>/<str:new_status>/', UpdateMaterialStatusView.as_view(), name='update_material_status'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
]