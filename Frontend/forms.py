# # from django import forms
# # from .models import Party

# # class PartyForm(forms.ModelForm):
# #     class Meta:
# #         model = Party
# #         fields = ["name", "phone", "address"]
# from django import forms
# from django.forms import inlineformset_factory
# from .models import JobCard, JobCardItem, JobcardQuotation, JobcardQuotationItem

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
