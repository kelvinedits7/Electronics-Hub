Electronics & Tech Hub - Starter (Stripe test + COD)

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
