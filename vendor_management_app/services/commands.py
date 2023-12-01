from vendor_management_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from datetime import datetime
from django.utils import timezone
from django.db.models import Avg, Count


def create_vendor(name:str, contact_details:str, address:str, vendor_code:str, on_time_delivery_rate:float, quality_rating_avg:float, average_response_time:float, fulfillment_rate:float) -> Vendor:
    vendor = Vendor.objects.create(
    name=name,
    contact_details=contact_details,
    address=address,
    vendor_code=vendor_code,
    on_time_delivery_rate=on_time_delivery_rate,
    quality_rating_avg=quality_rating_avg,
    average_response_time=average_response_time,
    fulfillment_rate=fulfillment_rate,
    )
    return vendor
def update_vendor(vendor: Vendor, name:str, contact_details:str, address:str, vendor_code:str, on_time_delivery_rate:float, quality_rating_avg:float, average_response_time:float, fulfillment_rate:float) -> Vendor:
    vendor.name=name
    vendor.contact_details=contact_details
    vendor.address=address
    vendor.vendor_code=vendor_code
    vendor.on_time_delivery_rate=on_time_delivery_rate
    vendor.quality_rating_avg=quality_rating_avg
    vendor.average_response_time=average_response_time
    vendor.fulfillment_rate=fulfillment_rate

    vendor.save()
    return vendor

def delete_vendor(vendor: Vendor) -> None:
    vendor.delete()
    return

# Here i have defined a backend logic
def update_historical_performance_metrics(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_orders = PurchaseOrder.objects.filter(vendor=vendor)

    on_time_delivery_rate = completed_orders.filter(delivery_date__lte=timezone.now()).count() / completed_orders.count() * 100 if completed_orders.count() > 0 else 0

    quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] if completed_orders.count() > 0 else 0

    response_times = completed_orders.exclude(acknowledgment_date=None).annotate(response_time=Count('acknowledgment_date', distinct=True))
    average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg'] if response_times.count() > 0 else 0

    fulfilment_rate = completed_orders.filter(status='completed').count() / total_orders.count() * 100 if total_orders.count() > 0 else 0

    historical_performance = HistoricalPerformance.objects.filter(vendor=vendor).first()
    if historical_performance:
        update_historical_performance(
            historical_performance,
            vendor_id=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfilment_rate
        )
    else:
        create_historical_performance(
            vendor_id=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfilment_rate
        )

def create_purchase_order(po_number:str, vendor:Vendor, order_date:datetime, delivery_date:datetime, items:str, quantity:int, status:str, quality_rating:float, issue_date:datetime, acknowledgment_date:datetime) -> PurchaseOrder:
    purchase_order = PurchaseOrder.objects.create(
        po_number=po_number,
        vendor=vendor,
        order_date=order_date,
        delivery_date=delivery_date,
        items=items,
        quantity=quantity,
        status=status,
        quality_rating=quality_rating,
        issue_date=issue_date,
        acknowledgment_date=acknowledgment_date,
    )

    update_historical_performance_metrics(vendor)

    return purchase_order
def update_purchase_order(purchase_order: PurchaseOrder, po_number:str, vendor:Vendor, order_date:datetime, delivery_date:datetime, items:str, quantity:int, status:str, quality_rating:float, issue_date:datetime, acknowledgment_date:datetime) -> PurchaseOrder:
    purchase_order.po_number=po_number
    purchase_order.vendor=vendor
    purchase_order.order_date=order_date
    purchase_order.delivery_date=delivery_date
    purchase_order.items=items
    purchase_order.quantity=quantity
    purchase_order.status=status
    purchase_order.quality_rating=quality_rating
    purchase_order.issue_date=issue_date
    purchase_order.acknowledgment_date=acknowledgment_date

    purchase_order.save()

    update_historical_performance_metrics(vendor)
    return purchase_order

def delete_purchase_order(purchase_order: PurchaseOrder) -> None:
    vendor = purchase_order.vendor
    purchase_order.delete()

    update_historical_performance_metrics(vendor)

    return


def create_historical_performance(vendor_id:Vendor, date:datetime, on_time_delivery_rate:float, quality_rating_avg:float, average_response_time:float, fulfillment_rate:float) -> HistoricalPerformance:
    historical_performance = HistoricalPerformance.objects.create(
    vendor=vendor_id,
    date=date,
    on_time_delivery_rate=on_time_delivery_rate,
    quality_rating_avg=quality_rating_avg,
    average_response_time=average_response_time,
    fulfillment_rate=fulfillment_rate,
    )
    return historical_performance

def update_historical_performance(historical_performance: HistoricalPerformance, vendor_id:Vendor, date:datetime, on_time_delivery_rate:float, quality_rating_avg:float, average_response_time:float, fulfillment_rate:float) -> HistoricalPerformance:

    historical_performance.vendor=vendor_id
    historical_performance.date=date
    historical_performance.on_time_delivery_rate=on_time_delivery_rate
    historical_performance.quality_rating_avg=quality_rating_avg
    historical_performance.average_response_time=average_response_time
    historical_performance.fulfillment_rate=fulfillment_rate

    historical_performance.save()
    return historical_performance
def delete_historical_performance(historical_performance: HistoricalPerformance) -> None:
    historical_performance.delete()
    return