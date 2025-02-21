from django.urls import path
from .views import Index, SignUpView, SignInView, CustomLogoutView, Dashboard, AddItem, EditItem, DeleteItem, request_material, material_orders, update_material_status, profile

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item', AddItem.as_view(), name='add-item'),
    path('Profile/', profile, name='profile'),
    path('request-material/', request_material, name='request_material'),
    path('update_material_status/<int:order_id>/<str:new_status>/', update_material_status, name='update_material_status'),
    path('material-orders/', material_orders, name='material_orders'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', CustomLogoutView.as_view(template_name='Inventory/logout.html'), name='logout'),
]
