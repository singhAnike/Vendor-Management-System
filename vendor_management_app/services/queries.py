from vendor_management_app.models import Vendor, PurchaseOrder, HistoricalPerformance

def get_vendors() -> Vendor:
    return Vendor.objects.all()

def get_purchase_orders() -> PurchaseOrder:
    return PurchaseOrder.objects.all()

def get_historical_performances() -> HistoricalPerformance:
    return HistoricalPerformance.objects.all()