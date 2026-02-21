from django import forms
from .models import JobCard, Quotation, QuotationItem, Party


# ===== Party Form =====
class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ["name", "phone", "address"]


# ===== JobCard Form =====
class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = "__all__"


# ===== Quotation Form =====
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'date',
            'customer_name',
            'customer_po_no',
            'job_type',
            'fabric_type',
            'payment_terms',
            'order_by',
            'style_no',
            'style_name',
            'combo',
            'image',
            'total_qty',
            'total_value'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# ===== Quotation Item Form =====
class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = [
            'particulars',
            'width',
            'height',
            'rate',
            'amt',
            'confirmed_amt',
            'qty',
            'value'
        ]















# from django import forms
# from .models import Quotation, QuotationItem 
#  # <-- use QuotationItem, NOT QuotationItemForm


# from django import forms
# from django.forms import inlineformset_factory
# from .models import JobCard, JobCardItem, JobcardQuotation, JobcardQuotationItem

# from .models import Party

# class PartyForm(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ["name", "phone", "address"]


# # from django import forms
# # from django.forms import inlineformset_factory
# # from .models import JobCard, JobCardItem, JobcardQuotation, JobcardQuotationItem

# class JobCardForm(forms.ModelForm):
#     class Meta:
#         model = JobCard
#         fields = ["date", "party", "job_type", "status", "remarks"]

# JobCardItemFormSet = inlineformset_factory(
#     JobCard, JobCardItem,
#     fields=["description", "qty", "rate"],
#     extra=1, can_delete=True
# )


# class QuotationForm(forms.ModelForm):
#     class Meta:
#         model = JobcardQuotation
#         fields = ["date", "party", "job_type", "status"]

# QuotationItemFormSet = inlineformset_factory(
#     JobcardQuotation, JobcardQuotationItem,
#     fields=["description", "qty", "rate"],
#     extra=1, can_delete=True
# )





# ===== Quotation Form =====
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'date', 'customer_name', 'customer_po_no',
            'job_type','fabric_type', 'payment_terms', 'order_by', 'style_no',
            'style_name', 'combo', 'image', 'total_qty', 'total_value'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Customer Name'}),
            # 'created_by': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customer_po_no': forms.TextInput(attrs={'placeholder': 'PO Number'}),
            'job_type': forms.Select(choices=[('Production','Production'), ('Reproduction','Reproduction')]),
            'fabric_type': forms.Select(choices=[('Cotton','Cotton'), ('Polyester','Polyester')]),
            'payment_terms': forms.Select(choices=[('Cash','Cash'), ('Credit','Credit')]),
            'order_by': forms.TextInput(attrs={'placeholder': 'Order By'}),
            'style_no': forms.TextInput(attrs={'placeholder': 'Style No'}),
            'style_name': forms.TextInput(attrs={'placeholder': 'Style Name'}),
            'combo': forms.TextInput(attrs={'placeholder': 'Combo'}),
        }

# ===== Quotation Item Form (for table entries) =====
class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem  # <-- correct model
        fields = [
            'particulars', 'width', 'height', 'rate', 'amt',
            'confirmed_amt', 'qty', 'value'
        ]
        widgets = {
            'particulars': forms.TextInput(attrs={'placeholder': 'Particulars'}),
            'width': forms.NumberInput(attrs={'step': '0.01'}),
            'height': forms.NumberInput(attrs={'step': '0.01'}),
            'rate': forms.NumberInput(attrs={'step': '0.01'}),
            'amt': forms.NumberInput(attrs={'step': '0.01'}),
            'confirmed_amt': forms.NumberInput(attrs={'step': '0.01'}),
            'qty': forms.NumberInput(),
            'value': forms.NumberInput(attrs={'step': '0.01'}),
        }
             
