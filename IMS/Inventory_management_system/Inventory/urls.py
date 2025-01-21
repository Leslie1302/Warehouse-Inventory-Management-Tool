from django.urls import path
from .views import Index, SignUpView, SignInView, CustomLogoutView, Dashboard, AddItem, EditItem, DeleteItem

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item', AddItem.as_view(), name='add-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', CustomLogoutView.as_view(template_name='Inventory/logout.html'), name='logout'),
]
