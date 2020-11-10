from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('dash', views.dash),
    path('edit_account/<int:user_id>',views.edit_account),
    path('create_quote', views.create_quote),
    path('logout', views.logout),
    path('user_quotes/<int:user_id>', views.user_quotes),
    path('delete/<int:quote_id>',views.delete_quote),
    path('update_user/<int:user_id>', views.update),
    path('like/<int:user_id>/<int:quote_id>', views.like)
]