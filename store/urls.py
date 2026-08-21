from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalogo/", views.catalog, name="catalog"),
    path("carrito/", views.cart, name="cart"),
    path("carrito/agregar/<slug:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("carrito/sumar/<slug:product_id>/", views.increase_quantity, name="increase_quantity"),
    path("carrito/restar/<slug:product_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("carrito/eliminar/<slug:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("pago/", views.checkout, name="checkout"),
    path("pago/confirmar/", views.confirm_order, name="confirm_order"),
]
