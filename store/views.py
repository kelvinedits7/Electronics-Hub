from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Banner, Cart, CartItem, Order, Review
from .forms import SignUpForm, ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.contrib.auth.forms import UserCreationForm
import stripe, random
from django.contrib.auth.models import User

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)

def home(request):
    banners = Banner.objects.filter(is_active=True)
    featured = Product.objects.filter(is_featured=True)
    categories = Category.objects.all()  # 👈 fetch categories

    if not featured.exists():
        featured = Product.objects.all().order_by('-created_at')[:8]

    context = {
        'banners': banners,
        'featured': featured,
        'categories': categories  # 👈 send to template
    }
    return render(request, 'store/home.html', context)



def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    
    # Search functionality
    query = request.GET.get('q')  # 'q' should match the search input name in your template
    if query:
        products = products.filter(name__icontains=query)

    # Category filtering
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    categories = Category.objects.all()  # So you can display categories in the template

    return render(request, 'store/product_list.html', {
        'products': products,
        'category': category,
        'categories': categories,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()

    # If no reviews, create some dummy ones
    if not reviews.exists():
        dummy_users = ["john_doe", "mary_smith", "tech_guru"]
        dummy_comments = [
            "Great product, totally worth it!",
            "Decent quality for the price.",
            "Exceeded my expectations!",
            "Not bad, could be better.",
            "Fantastic, highly recommend!"
        ]

        for username in dummy_users:
            user, _ = User.objects.get_or_create(username=username)
            Review.objects.create(
                product=product,
                user=user,
                rating=random.randint(3, 5),  # between 3 and 5 stars
                comment=random.choice(dummy_comments)
            )

        reviews = product.reviews.all()  # reload reviews after adding

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # Handle posting a review
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")
        if request.user.is_authenticated and rating:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return redirect('product_detail', slug=product.slug)

    return render(request, "store/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "related_products": related_products
    })
    
def product_search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(brand__icontains=query)
    )
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'store/search_results.html', context)    

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in the user after signup
            return redirect("home")  # change "home" to your homepage url name
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

# Cart & Checkout
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Added to cart', 'cart_count': cart.items.count()})
    
    messages.success(request, 'Added to cart')
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('home')
    
    if request.method == 'POST':
        method = request.POST.get('payment_method', 'cod')
        if method == 'cod':
            order = Order.objects.create(user=request.user, total_amount=cart.get_total(), payment_method='cod', paid=False)
            cart.items.all().delete()
            return redirect('order_success')
        elif method == 'stripe':
            total_cents = int(cart.get_total() * 100)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'Order for {request.user.username}'},
                        'unit_amount': total_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/order-success/'),
                cancel_url=request.build_absolute_uri('/cart/'),
            )
            order = Order.objects.create(user=request.user, total_amount=cart.get_total(), payment_method='stripe', stripe_payment_id=session.id, paid=False)
            return redirect(session.url, code=303)
    
    return render(request, 'store/checkout.html', {'cart': cart})

def order_success(request):
    return render(request, 'store/order_success.html')
