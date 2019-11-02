from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# 0-inactive, 1-person, 2-partner, 3-leader, 4-manager, 5-director, 6-millioner
class Node(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)
    address = models.CharField(max_length=60, null=True)
    status = models.IntegerField(default=0, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    step = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    inviter = models.ForeignKey("Node", null=True, blank=True, related_name='invited_children', on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_processed = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.user.username + get_status(self.status)


def get_status(status):
    if status == 0:
        return "    (неактивный)"
    if status == 1:
        return "    (classic)"
    if status == 2:
        return "    (Партнер)"
    if status == 3:
        return "    (Лидер)"
    if status == 4:
        return "    (Менеджер)"
    if status == 5:
        return "    (Директор)"
    if status == 6:
        return "    (Миллионер)"
    return ""


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
    currency = models.CharField(max_length=20, null=True, blank=True)
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


class PropertyValueSettings(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name
