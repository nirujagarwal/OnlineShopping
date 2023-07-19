from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("contact/", views.contact, name="ContactUs"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProdView"),
    path("checkout/", views.checkout, name="Checkout"),

]

