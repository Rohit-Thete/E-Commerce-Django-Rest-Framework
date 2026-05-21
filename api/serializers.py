from .models import User, Product, Category, Order, OrderItem
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is In-Active")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]

    def validate_username(self, value):
        user = self.instance
        if " " in value:
            raise serializers.ValidationError("Username Cannot contain Spaces")
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already exists")

        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(), message="This Category already exists"
            )
        ]
    )

    class Meta:
        model = Category
        fields = "__all__"

    # def validate_name(self,value):
    #     category = self.instance
    #     if category:

    #         exists = Category.objects.filter(name=value).exclude(id=category.id).exists()
    #     else:

    #         exists = Category.objects.filter(name=value).exists()

    #     if exists:
    #         raise serializers.ValidationError("This Category already exists")

    #     return value


class ProductWriteSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source = "category.name")
    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("price should be greater than 0")

        return value

    # def create(self, validated_data):
    #     category_data = validated_data.pop("category")
    #     category, _ = Category.objects.get_or_create(**category_data)

    #     product = Product.objects.create(category=category, **validated_data)
    #     return product


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)


class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "quantity", "price", "item_subtotal"]


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "total_bill", "items", "created_at", "status"]
