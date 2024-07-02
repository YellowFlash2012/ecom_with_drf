from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.pagination import PageNumberPagination
import stripe.error
import stripe.webhook

from .models import *
from .serializers import *
from .filters import *
from products.models import Product

from rest_framework.pagination import PageNumberPagination

import stripe
import os
from eshop.utils.helpers import *

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    
    # filter config
    filterset = OrdersFilter(request.GET, queryset=Order.objects.all().order_by('id'))
    
    count = filterset.qs.count()
    
    # pagination config
    resPerPage = 9
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    
    queryset = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = OrderSerializer(queryset, many=True)
    
    return Response({"success":True, "count":len(serializer.data), "page":resPerPage, "message":"Here are all the orders you placed on our site", "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_single_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    serializer = OrderSerializer(order, many=False)
    
    return Response({"success":True, "message":"Here is the order you requested", "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    
    order_items = data["orderItems"]
    
    if order_items and len(order_items) == 0:
        return Response({"error":"Your cart is empty. Kindly add at least 1 product!"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        
        order = Order.objects.create(
            user=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_number=data['phone_number'],
            country=data['country'],
            total_amount=total_amount
        )
        
        # create order item and set order to order item
        for i in order_items:
            product = Product.objects.get(id=i["product"])
            
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price']
            )
            
            # update product qty
            product.stock -= item.quantity
            product.save()
        
        serializer = OrderSerializer(order, many=False)
        
        return Response({"success":True, "message":"Order placed successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)

# process order
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_single_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    order.order_status = request.data["order_status"]
    
    serializer = OrderSerializer(order, many=False)
    
    return Response({"success":True, "message":f"Order {order.id} has been successfully processed", "data":serializer.data}, status=status.HTTP_201_CREATED)

# process order
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_single_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    order.delete()
    
    return Response({"success":True, "message":f"Order {order.id} has been successfully deleted"}, status=status.HTTP_200_OK)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    user = request.user
    data = request.data
    
    YOUR_DOMAIN = get_current_host(request)
    
    order_items = data["orderItems"]
    
    shipping_details = {
        "street":data["street"],
        "city":data["city"],
        "state":data["state"],
        "zip_code":data["zip_code"],
        "phone_number":data["phone_number"],
        "country":data["country"],
        "user":user.id
    }
    
    checkout_order_items = []
    for item in order_items:
        checkout_order_items.append({
            "price_data":{
                "currency":"usd",
                "product_data":{
                    "name":item['name'],
                    "images":[item['image']],
                    "metadata":{"product_id":item['product']}
                },
                "unit_amount":item['price'] *  100
            },
            "quantity":item["quantity"]
        })
        
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        metadata=shipping_details,
        line_items=checkout_order_items,
        customer_email=user.email,
        mode="payment",
        success_url=YOUR_DOMAIN,
        cancel_url=YOUR_DOMAIN
    )
    
    return Response({"success":True, "message":"Checkout session successfully created!", "session":session}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stripe_webhook(request):
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    payload=request.body
    sig_header=request.META['HTTP_STRIPE_SIGNATURE']
    event=None
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return Response({"success":False, "error":"Invalid payload!"}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.SignatureVerificationError as e:
        return Response({"success":False, "error":"Invalid signature!"}, status=status.HTTP_400_BAD_REQUEST)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        
        return Response({"success":True, "message":'Your Payment was successful'})
    