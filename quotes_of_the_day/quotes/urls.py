from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_quote, name="quote"),
    path('quote/<int:quote_id>/reaction/',views.react_to_quote, name="quote_reaction"),
    path('add/', views.add_quote, name="add_quote"),
    path('top_quotes/', views.get_top_quotes, name="top_quotes"),
]