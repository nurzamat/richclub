from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Node(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)
    address = models.CharField(max_length=60, null=True)
    status = models.IntegerField(default=0, null=True)  # 1-active, 0-free
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    step = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    inviter = models.ForeignKey("Node", null=True, blank=True, related_name='invited_children', on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.user.username


class BonusType(models.Model):
    code = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="bonus_node", null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    partner = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="bonus_partner", null=True)
    type = models.CharField(max_length=60, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.value


class BonusSettings(models.Model):
    bonus_type = models.ForeignKey(BonusType, on_delete=models.CASCADE)
    bonus_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    level = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.bonus_type.name


