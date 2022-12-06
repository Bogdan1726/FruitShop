from django.urls import path
from .views import transactions, audit, warehouse, MainPage

urlpatterns = [
    path('', MainPage.as_view(), name='home'),

    # ajax
    path('transactions/', transactions, name='transactions'),
    path('warehouse/', warehouse, name='warehouse'),
    path('audit/', audit, name='audit'),
]
