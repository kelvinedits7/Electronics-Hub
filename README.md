Electronics & Tech Hub - Starter (Stripe test + COD)....
Electronics Hub is a full-featured e-commerce web application built with Django. Users can browse products, view product details, add items to the cart, checkout, and see an order confirmation. The project includes an admin panel for managing products, categories, and reviews, and supports currency display for product prices.

Features
-User authentication: Sign up, login, and logout
-Product listing and categories
-Product detail view with quantity selection
-Add to cart, remove from cart, and view cart
-Checkout with simulated payment (Stripe test keys)
-Related products section
-Admin panel for managing products, categories, and reviews
-Product search functionality
-Responsive UI using Bootstrap

Technologies Used
-Backend: Python 3.13.5, Django 5.2.6
-Frontend: HTML, CSS, Bootstrap
-Database: SQLite3 (for development)
-Other: Django Crispy Forms, Django Decouple for environment variables

Setup:
1. Create and activate venv
   python -m venv venv
   # Windows PowerShell:
   venv\Scripts\Activate
   # mac/linux:
   source venv/bin/activate

2. Install deps
   pip install -r requirements.txt

3. (Optional) Add Stripe test keys in electronics_hub/settings.py:
   STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
   STRIPE_SECRET_KEY = 'sk_test_...'

4. Run migrations and create superuser:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

5. Run server:
   python manage.py runserver

6. Admin: http://127.0.0.1:8000/admin/ - add Categories, Products, Banners, then test site.


Group Name: E-Shop Innovators
Group Members:
1. Dakey Kelvin Kojo - 01241471B
2. James Agbesi - 01242068B
3. Agu Tamakloe Jerry - 01242453B 
4. Lartey Richmond - 01241423B
5. Taha Abiba Boyo - 01243278B


