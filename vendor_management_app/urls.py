from django.urls import path
from vendor_management_app import views

urlpatterns = [

    path('vendors/', views.VendorApi.as_view()),
    path('vendors/<int:vendor_id>/', views.VendorApi.as_view()),
    path('purchase_orders/', views.PurchaseOrderApi.as_view()),
    path('purchase_orders/', views.PurchaseOrderApi.as_view()),
    path('purchase_orders/<int:po_id>/', views.PurchaseOrderApi.as_view()),
    path('purchase_orders/<int:po_id>/acknowledge/', views.AcknowledgePurchaseOrder.as_view()),
    path('vendors/<int:vendor_id>/performance', views.HistoricalPerformanceApi.as_view()),    

]
