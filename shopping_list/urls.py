from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_shopping_lists, name='list_shopping_lists'),
    path('add/', views.add_shopping_list, name='add_shopping_list'),
    path('add_item/<int:list_id>/', views.add_item_to_list, name='add_item_to_list'),
    path('edit/<int:list_id>/', views.edit_shopping_list, name='edit_shopping_list'),
    path('delete/<int:list_id>/', views.delete_shopping_list, name='delete_shopping_list'),
    path('report/', views.report_view, name='report_view'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),  # Ensure this is present
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]