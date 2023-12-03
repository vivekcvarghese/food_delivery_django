from django.urls import path
from app.views import ProductDetail, ProductList, AddUser, OrderResource

urlpatterns = [
    path('product/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),
    path('product/', ProductDetail.as_view(), name='product'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('user/<int:user_id>/', AddUser.as_view(), name='user'),
    path('users/', AddUser.as_view(), name='user-list'),
    path('order/<int:order_id>/', OrderResource.as_view(), name='order'),
    path('order/', OrderResource.as_view(), name='order')
    
]