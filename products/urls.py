from django.urls import path, include
from products import views

urlpatterns = [
    path("", views.index),
    path("list", views.catalog),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("book/<int:product_id>/", views.book_car, name="book_car"),
    path("booked_dates/<int:product_id>/", views.booking_dates, name="booking_dates"),
    path("booked/<int:product_id>/", views.booked_dates, name="booked_dates"),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-panel/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path("booking/<int:pk>/delete/", views.booking_delete, name="booking_delete"),
    path("booking/<int:pk>/edit/", views.booking_edit, name="booking_edit"),
    path("product/<int:product_id>/toggle_favorite/", views.toggle_favorite, name="toggle_favorite"),
    path('favorites/', views.favorite_list, name='favorite_list'),

]
