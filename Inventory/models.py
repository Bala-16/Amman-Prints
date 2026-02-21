from django.db import models
from django.utils import timezone
from decimal import Decimal


# ============================================================================
# JOBCARD MODEL - ✅ FIXED
# ============================================================================

class JobCard(models.Model):
    jobcard_no = models.CharField(max_length=50, unique=True, db_index=True)
    date = models.DateTimeField()  # required

    order_by = models.CharField(max_length=200, blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    style_no = models.CharField(max_length=100)
    job_created_by = models.CharField(max_length=100, default="admin")
    style_name = models.CharField(max_length=200)
    customer_po_no = models.CharField(max_length=100, blank=True, null=True)
    combo = models.CharField(max_length=100)

    job_type = models.CharField(max_length=50, blank=True, null=True)
    fabric_type = models.CharField(max_length=100, blank=True, null=True, default="N/A")
    designer_name = models.CharField(max_length=100)
    hsn_code = models.CharField(max_length=20, default="998821")

    # JSON items (store line items)
    items = models.JSONField(default=list, blank=True, null=True)

    # totals
    total_qty = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    avg_rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0.0000"))
    l_confirm_rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0.0000"))
    h_confirm_rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0.0000"))

    mistake_details = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    approval = models.CharField(max_length=50, default="Pending")
    status = models.CharField(max_length=50, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_jobcard"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["jobcard_no"]),
            models.Index(fields=["customer_name"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.jobcard_no} - {self.customer_name}"


# ============================================================================
# DOCUMENT SEQUENCE MODEL
# ============================================================================

class DocSequence(models.Model):
    """
    For generating sequential document numbers
    """
    doc_type = models.CharField(max_length=10)
    yymm = models.CharField(max_length=4)
    last_no = models.PositiveIntegerField(default=0)
    # ✅ FIXED: auto_now_add instead of default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_docsequence'
        unique_together = ("doc_type", "yymm")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.doc_type}-{self.yymm}-{self.last_no}"


# ============================================================================
# PARTY MODEL - ✅ FIXED
# ============================================================================

class Party(models.Model):
    """
    Customer/Party Master
    """
    party_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    gst_no = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # ✅ FIXED: auto_now_add instead of default=timezone.now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_party'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['party_no']),
        ]

    def __str__(self):
        return f"{self.party_no} - {self.name}"


# ============================================================================
# QUOTATION MODEL - ✅ FIXED
# ============================================================================

class Quotation(models.Model):
    """
    Quotation Model for customer quotations
    """
    date = models.DateTimeField()
    
    quotation_no = models.CharField(max_length=50, unique=True, db_index=True)
    customer_name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=100)
    customer_po_no = models.CharField(max_length=100, blank=True, null=True)
    
    job_type = models.CharField(
        max_length=50,
        choices=[
            ("Production", "Production"),
            ("Reproduction", "Reproduction"),
            ("Sample", "Sample"),
            ("Sticker", "Sticker"),
        ],
        default="Production"
    )
    
    fabric_type = models.CharField(
        max_length=100,
        default="Domestic",
        blank=True,
        null=True
    )
    
    payment_terms = models.CharField(
        max_length=50,
        choices=[("Cash", "Cash"), ("Credit", "Credit")],
        default="Cash",
        blank=True,
        null=True
    )
    
    order_by = models.CharField(max_length=200, blank=True, null=True)
    style_no = models.CharField(max_length=100)
    style_name = models.CharField(max_length=200)
    combo = models.CharField(max_length=100)
    image = models.ImageField(upload_to='quotations/', blank=True, null=True)
    
    # Totals - ✅ Using Decimal
    total_qty = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Status
    status = models.CharField(max_length=50, default='Pending')
    # ✅ FIXED: auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inventory_quotation'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['quotation_no']),
            models.Index(fields=['customer_name']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.quotation_no} - {self.customer_name}"


# ============================================================================
# QUOTATION ITEM MODEL - ✅ FIXED
# ============================================================================

class QuotationItem(models.Model):
    """
    Quotation Items (Line Items)
    """
    quotation = models.ForeignKey(
        Quotation, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    particulars = models.CharField(max_length=200)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    height = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.0000'))
    amt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    confirmed_amt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    # ✅ FIXED: auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_quotationitem'
        ordering = ['id']

    def __str__(self):
        return f"{self.particulars} ({self.quotation.quotation_no})"


# ============================================================================
# JOBCARD ITEM MODEL (Optional) - ✅ FIXED
# ============================================================================

class JobCardItem(models.Model):
    """
    Optional: JobCard Items (if you don't want to use JSONField)
    Currently not used - JobCard uses JSONField for items
    """
    jobcard = models.ForeignKey(
        JobCard, 
        on_delete=models.CASCADE, 
        related_name='items_rel'
    )
    particulars = models.CharField(max_length=200)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    height = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.0000'))
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    sq_inch = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    confirmed_amt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    confirmed_rate = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.0000'))
    value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    # ✅ FIXED: auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_jobcarditem'
        ordering = ['id']

    def __str__(self):
        return f"{self.jobcard.jobcard_no} - {self.particulars}"