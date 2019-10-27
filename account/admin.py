from django.contrib import admin

from .models import Node, BonusType, BonusSettings, PropertyValueSettings

admin.site.register(Node)
admin.site.register(BonusType)
admin.site.register(BonusSettings)
admin.site.register(PropertyValueSettings)

