from django.urls import path
from .views import OrderCreateView,MyOrderListView,AllOrdersListView,OrderStatusUpdateView
urlpatterns = [
    path('',OrderCreateView.as_view(),name='create-order'),
    path('my-orders/',MyOrderListView.as_view(),name='my-orders'),
    path('all-orders/',AllOrdersListView.as_view(),name='all-orders'),
    path('<uuid:pk>/status/',OrderStatusUpdateView.as_view(),name='update-order-status')
]