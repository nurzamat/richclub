from django.contrib import admin

from .models import Node, BonusType, BonusSettings


admin.site.register(Node)
admin.site.register(BonusType)
admin.site.register(BonusSettings)

