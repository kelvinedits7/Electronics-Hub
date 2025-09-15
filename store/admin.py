from django.contrib import admin
from .models import Category, Product, Banner, Cart, CartItem, Order, ProductImage

# --- CategoryAdmin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# --- Inline for Product Images ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # how many empty image slots to show by default

# --- ProductAdmin with bulk action + inline images ---
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
make_featured.short_description = "Mark selected products as featured"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    actions = [make_featured]
    inlines = [ProductImageInline]  # <-- shows extra images inline

# --- Other admins ---
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_amount','payment_method','paid','created_at')
