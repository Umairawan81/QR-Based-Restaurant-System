
from django.urls import path 
from . import views
urlpatterns = [
    path('', views.Login , name='login'),
    path('menu', views.MenuView , name='menu'),
    path('edit-menu/', views.EditMenu , name='edit'),
    path('order/<int:pk>/', views.OrderGet , name='get_order'),
    path('order-confirm/<int:pk>/' , views.ConfirmOrder , name='con_order'),
    path('nav/' , views.navbar ,name='nav'),
    path('Update-Item/' , views.UpdateItem , name='Update_item'),
    path('del-items/<int:pk>/' , views.DelItem , name='del_items'),
    path('confirmed-order/' , views.ConfirmedOrd , name='final_order'),
    path('Comp-ord/<int:pk>/' , views.CompletedOrder , name='comp'),
    path('Edit-items/<int:pk>/' , views.EditItem , name='edit_item'),
    path('Remove-items/<int:pk>/' , views.RemoveItem , name='rem_item'),
    path('dashboard/', views.DashBoard , name='dash'),
    path('QR/', views.QR , name='qr'),
    path('ty/', views.Thanks , name='ty'),

   
]