from django.contrib import admin
from .models import Flat, Complaint, Owner


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'address', 'owner')
    readonly_fields = ('created_at', )
    list_display = (
        'address',
        'price',
        'new_building',
        'construction_year',
        'town',
        'owners_phonenumber',
        'owner_phone_pure'
        )
    list_editable = ('new_building', )
    list_filter = ('new_building', 'rooms_number', 'has_balcony', 'active')
    raw_id_fields = ('liked_by', )

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('flat', )
    list_display = ('user', 'flat', 'text')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('flats', )
    list_display = ('owner', 'owner_phone_pure')
