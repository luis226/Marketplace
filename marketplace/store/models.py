from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


class User(AbstractUser):
    USER_BUYER = 'buyer'
    USER_SELLER = 'seller'
    USER_TYPES = (
        (USER_BUYER,'A user which uses the platform for buying products'),
        (USER_SELLER, 'A user which uses the platform for selling products')
    )

    SEX_MALE = 'male'
    SEX_FEMALE = 'female'
    SEXS = (
        (SEX_MALE, 'User is male'),
        (SEX_FEMALE,'User is female')
    )

    # I think is better to use uuid insted of user_id in the UI, because user_id 
    # might leak unwanted information
    uuid = models.UUIDField(default=uuid4, unique=True)

    sex = models.CharField(choices=SEXS, null=False, blank=False, max_length=10, default=USER_BUYER)

    type = models.CharField(choices=USER_TYPES, null=False, blank=False, max_length=20, default=SEX_MALE)

class Product(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)

    price = models.DecimalField(
        null=False, blank=False, validators=[MinValueValidator(0)],
        max_digits=6, decimal_places=2
    )

    selled_by = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)

    stock = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, null=False, blank=False)

    description = models.CharField(max_length=1000)

class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)

    product = models.OneToOneField(Product, null=False, blank=False, on_delete=models.PROTECT)

    units = models.IntegerField(validators=[MinValueValidator(1)])

    STATUS = (
        ('cart', 'The product is in the buyer cart'),
        ('ordered', 'The product is ordered by the user but not paid yet'),
        ('payed', 'The product is payed already'),
        ('cancelled', 'The product order is cancelled')
    )

    status = models.CharField(choices=STATUS, max_length=50)

    buyer = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now=True, null=False, blank=False)

    modified = models.DateTimeField(blank=True, null=True)

