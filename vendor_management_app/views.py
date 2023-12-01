from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from vendor_management_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from vendor_management_app.services.commands import (
    create_vendor, update_vendor, delete_vendor,
    create_purchase_order, update_purchase_order, delete_purchase_order,
    create_historical_performance, update_historical_performance, delete_historical_performance, update_historical_performance_metrics
)
from vendor_management_app.services.queries import (
    get_vendors, get_purchase_orders, get_historical_performances
)


class VendorApi(APIView):
    paginator = PageNumberPagination()

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vendor
            fields = ['name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    class OutputSerializer(serializers.ModelSerializer):
        vendor_id = serializers.IntegerField(source="id")

        class Meta:
            model = Vendor
            fields = ['vendor_id', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def get(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')

        if vendor_id:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            serializer = self.OutputSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        params = request.GET.dict()
        vendors = get_vendors()
        no_pagination = request.GET.get('no_pagination', False) == 'true'

        if no_pagination:
            return Response(self.OutputSerializer(vendors, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

        self.paginator.page_size = request.GET.get('count', 10)
        result_page = self.paginator.paginate_queryset(vendors, request)
        serializer = self.OutputSerializer(result_page, many=True, context={'request': request})
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = create_vendor(**serializer.validated_data)
        return Response(self.OutputSerializer(vendor).data, status=status.HTTP_201_CREATED)

    def put(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = update_vendor(vendor=vendor, **serializer.validated_data)
        return Response(self.OutputSerializer(vendor).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        delete_vendor(vendor=vendor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderApi(APIView):
    paginator = PageNumberPagination()

    class InputSerializer(serializers.ModelSerializer):
        vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

        class Meta:
            model = PurchaseOrder
            fields = ['po_number', 'vendor_id', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']

    class OutputSerializer(serializers.ModelSerializer):
        po_id = serializers.IntegerField(source="id")

        class Meta:
            model = PurchaseOrder
            fields = ['po_id', 'po_number', 'vendor_id', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']

    def get(self, request, *args, **kwargs):
        po_id = request.query_params.get('po_id')
        vendor_id = request.query_params.get('vendor_id')

        if po_id:
            purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
            serializer = self.OutputSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif 'po_id' in kwargs:
            purchase_order = get_object_or_404(PurchaseOrder, id=kwargs['po_id'])
            serializer = self.OutputSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
            serializer = self.OutputSerializer(purchase_orders, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            params = request.GET.dict()
            purchase_orders = get_purchase_orders()
            no_pagination = request.GET.get('no_pagination', False) == 'true'

            if no_pagination:
                return Response(self.OutputSerializer(purchase_orders, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

            self.paginator.page_size = request.GET.get('count', 10)
            result_page = self.paginator.paginate_queryset(purchase_orders, request)
            serializer = self.OutputSerializer(result_page, many=True, context={'request': request})
            return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.validated_data.pop('vendor_id', None)
        purchase_order = create_purchase_order(vendor=vendor, **serializer.validated_data)
        return Response(self.OutputSerializer(purchase_order).data, status=status.HTTP_201_CREATED)

    def put(self, request, po_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = update_purchase_order(purchase_order=purchase_order, **serializer.validated_data)
        return Response(self.OutputSerializer(purchase_order).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, po_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        delete_purchase_order(purchase_order=purchase_order)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)

        if purchase_order.acknowledgment_date:
            return Response({"detail": "Purchase order already acknowledged."},
                            status=status.HTTP_400_BAD_REQUEST)

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        update_historical_performance_metrics(purchase_order.vendor)

        return Response({"detail": "Purchase order acknowledged successfully."},
                        status=status.HTTP_200_OK)


class HistoricalPerformanceApi(APIView):
    paginator = PageNumberPagination()

    class InputSerializer(serializers.ModelSerializer):
        vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

        class Meta:
            model = HistoricalPerformance
            fields = ['vendor_id', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    class OutputSerializer(serializers.ModelSerializer):
        historical_performance_id = serializers.IntegerField(source="id")

        class Meta:
            model = HistoricalPerformance
            fields = ['historical_performance_id', 'vendor_id', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def get(self, request, *args, **kwargs):
        vendor_id = self.kwargs.get('vendor_id')

        if vendor_id:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            historical_performances = get_historical_performances(vendor)

            if historical_performances.exists():
                serializer = self.OutputSerializer(historical_performances, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"No historical performances found for vendor with ID {vendor_id}."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "vendor_id not provided in URL."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        historical_performance = create_historical_performance(**serializer.validated_data)
        return Response(self.OutputSerializer(historical_performance).data, status=status.HTTP_201_CREATED)

    def put(self, request, historical_performance_id, *args, **kwargs):
        historical_performance = get_object_or_404(HistoricalPerformance, id=historical_performance_id)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        historical_performance = update_historical_performance(historical_performance=historical_performance,
                                                                **serializer.validated_data)
        return Response(self.OutputSerializer(historical_performance).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, historical_performance_id, *args, **kwargs):
        historical_performance = get_object_or_404(HistoricalPerformance, id=historical_performance_id)

        delete_historical_performance(historical_performance=historical_performance)
        return Response(status=status.HTTP_204_NO_CONTENT)
