from django.contrib import admin
from django.urls import path, include
from store import views as store_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Store URLs
    path("", store_views.home, name="home"),
    path("products/", store_views.product_list, name="product_list"),
    path("category/<slug:category_slug>/", store_views.product_list, name="products_by_category"),
    path("product/<slug:slug>/", store_views.product_detail, name="product_detail"),
    path("cart/", store_views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", store_views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", store_views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", store_views.checkout, name="checkout"),
    path("order-success/", store_views.order_success, name="order_success"),
    path('search/', store_views.product_search, name='product_search'),


    # Authentication URLs
    path("accounts/signup/", store_views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),   # uses registration/login.html
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Other built-in auth URLs (password reset, change, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
