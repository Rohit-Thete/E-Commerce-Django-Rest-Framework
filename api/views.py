from django.shortcuts import render
from django.db.models import Prefetch
from .models import User, Category, Product, Order, OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
    CategorySerializer,
    ProductWriteSerializer,
    ProductReadSerializer,
    OrderCreateSerializer,
    OrderReadSerializer
)
from .service import create_order
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .permissions import *

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "msg": "User Created",
                "user": {"username": user.username, "email": user.email},
            },
            status=201,
        )

    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        return Response(
            {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
                "user": {"username": user.username, "email": user.email},
            },
            status=200,
        )

    return Response(serializer.errors, status=400)


class UserView(APIView):
    permission_classes = [IsOwner, IsAuthenticated]

    def get(self, request):
        user = request.user
        data = User.objects.get(username=user.username)

        serializer = UserReadSerializer(data)
        return Response(serializer.data, status=200)

    def put(self, request):
        user = request.user
        self.check_object_permissions(request, user)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class CategoryView(APIView):
    # permission_classes=([IsAuthenticated,IsAdmin])

    def get_permissions(self):
        if self.request.method in ["POST", "UPDATE", "DELETE"]:
            return [IsAuthenticated(), IsAdmin()]
        return [AllowAny()]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {"msg": "Category Added Successfully", "category": obj.name}, status=201
            )

        return Response(serializer.errors, status=400)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=200)

    def put(self, request, pk):
        catogory = Category.objects.get(id=pk)
        serializer = CategorySerializer(catogory, data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {"msg": "Category Updated Succeessfully", "category": obj.name},
                status=200,
            )

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = get_object_or_404(Category, id=pk)

        name = category.name
        category.delete()
        return Response({"msg": f"Category '{name}' deleted successfully"}, status=200)


class ProductView(APIView):
    def get_permissions(self):
        if self.request.method in ["POST", "UPDATE", "DELETE"]:
            return [IsAuthenticated(), IsAdmin()]
        return [AllowAny()]

    def post(self, request):
        serializer = ProductWriteSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {"msg": f"product '{obj.name}' saved successfully"}, status=201
            )

        return Response(serializer.errors, status=400)

    def get(self, request):
        products = Product.objects.select_related("category")
        serializer = ProductReadSerializer(products, many=True)

        return Response(serializer.data, status=200)

    def put(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductWriteSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {"msg": f"Product '{obj.name}' updated successfully"}, status=200
            )

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        name = product.name
        product.delete()

        return Response({"msg": f"Product '{name}' deleted succesfully"}, status=200)
    


class OrderView(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            items = serializer.validated_data["items"]

            order = create_order(request.user,items)

            return Response({"msg":"order created","orderid":order.id},status=201)
        
        return Response(serializer.errors,status=400)
    

    def get(self,request):
        user = request.user
        orders = Order.objects.filter(user = user).prefetch_related(Prefetch("items", queryset=OrderItem.objects.select_related("product")))
        serializer = OrderReadSerializer(orders,many=True)

        return Response(serializer.data,status=200)
    

    def delete(self,request,pk):
        user = request.user
        order = get_object_or_404(Order,id=pk,user=user)
        id = order.id
        order.delete()

        return Response({"msg":f"Order with id '{id}' deleted successfully"})



