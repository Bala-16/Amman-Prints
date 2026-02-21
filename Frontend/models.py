# from django.db import models

# class JobCard(models.Model):
#     # Basic Fields
#     jobcard_no = models.CharField(max_length=20, unique=True)
#     date = models.DateTimeField()
#     order_by = models.CharField(max_length=100, blank=True)
#     customer_name = models.CharField(max_length=100)
#     style_no = models.CharField(max_length=50)
#     job_created_by = models.CharField(max_length=50, default='admin')
#     style_name = models.CharField(max_length=100)
#     customer_po_no = models.CharField(max_length=50)
#     combo = models.CharField(max_length=50)
#     job_type = models.CharField(max_length=50, blank=True)
#     fabric_type = models.CharField(max_length=50, blank=True)
#     designer_name = models.CharField(max_length=100)
#     hsn_code = models.CharField(max_length=20, default='998821')
    
#     # ✅ Store calculated items as JSON (no separate table needed)
#     items = models.JSONField(default=list, blank=True)
    
#     # Calculated Totals
#     total_qty = models.IntegerField(default=0)
#     total_value = models.FloatField(default=0)
#     avg_rate = models.FloatField(default=0)
#     l_confirm_rate = models.FloatField(default=0)
#     h_confirm_rate = models.FloatField(default=0)
    
#     # Mistake Section
#     mistake_details = models.TextField(blank=True)
#     reason = models.TextField(blank=True)
    
#     # Status
#     approval = models.CharField(max_length=20, default='Pending')
#     status = models.CharField(max_length=20, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.jobcard_no