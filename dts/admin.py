from django.contrib import admin
from .models import Home, Portofolio, Price, Service, Contact, Partnership

class HomeAdmin(admin.ModelAdmin):
    list_display = ('image', 'active')
    list_filter = ('active',)

class PortofolioAdmin(admin.ModelAdmin):
    list_display = ('image',)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('level', 'price', 'features', 'special')
    list_filter = ('special',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

class PartnershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(Home, HomeAdmin)
admin.site.register(Portofolio, PortofolioAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Partnership, PartnershipAdmin)
