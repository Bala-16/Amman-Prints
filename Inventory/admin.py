# jobcard/admin.py
from django.contrib import admin
from .models import JobCard, Party, Quotation, QuotationItem

@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = ['jobcard_no', 'customer_name', 'status', 'created_at']

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['party_no', 'name', 'phone']