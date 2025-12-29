from django.urls import path

from . import views


urlpatterns = [
    path("shows/<int:show_id>/", views.show_detail, name="show_detail"),
    path("shows/<int:show_id>/checkout/", views.checkout, name="checkout"),
    path("shows/<int:show_id>/success/", views.checkout_success, name="checkout_success"),
]
