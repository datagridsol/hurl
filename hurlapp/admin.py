# dappx/admin.py
from django.contrib import admin
from hurlapp.models import Language,State,District,City,UserProfile,Order,Product,ManageContent,Notification,Support,SupportReply,Recharge,MobileLang,Scratch,OrderProductsDetail,LoyaltyPoints,UserLoyaltyPoints,UserLinkage
# Register your models here.
admin.site.register(Language)
admin.site.register(State)
admin.site.register(District)
admin.site.register(City)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ManageContent)
admin.site.register(Notification)
admin.site.register(Support)
admin.site.register(SupportReply)
admin.site.register(Recharge)
admin.site.register(MobileLang)
admin.site.register(Scratch)
admin.site.register(OrderProductsDetail)
admin.site.register(LoyaltyPoints)
admin.site.register(UserLoyaltyPoints)
admin.site.register(UserLinkage)
