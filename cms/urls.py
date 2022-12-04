from django.urls import path
from .views import index, transactions, audit, warehouse

urlpatterns = [
    path('', index, name='home'),

    # ajax
    path('transactions/', transactions, name='transactions'),
    path('warehouse/', warehouse, name='warehouse'),
    path('audit/', audit, name='audit'),
]

