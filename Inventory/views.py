from django.shortcuts import render
from django.http import HttpResponse


def nav(request):
    return render(request,'nav.html')

def customer_report(request):
    return render(request,'jobcard/customer_report.html')
def quotation(request):
    return render(request,'jobcard/quotation.html',)
def designer_report(request):
    return render(request,'jobcard/designer_report.html',)
def process_report(request):
    return render(request,'jobcard/process_report.html',)
def quotation_customer(request):
    return render(request,'jobcard/quotation_customer.html',)
def job_creation(request):
    return render(request,'jobcard/job_creation.html',)
def job_list(request):
    return render(request,'jobcard/job_list.html',)
def quotation_form(request):
    return render(request,'jobcard/quotation_form.html',)


def company_creation(request):
    return render(request,'mastercreation/company_creation.html',)
def party_creation(request):
    return render(request,'mastercreation/party_creation.html',)
def user_type_creation(request):
    return render(request,'mastercreation/user_type_creation.html',)
def fusing(request):
    return render(request,'fusing/fusing.html',)
def printing(request):
    return render(request,'printing/printing.html',)
def consumable(request):
    return render(request,'consumable/consumable.html',)
def accounts(request):
    return render(request,'accounts/accounts.html',)
def  delivery(request):
    return render(request,'delivery/delivery.html',)
def dashboard(request):
    return render(request,'dashboard/dashboard.html',)




def operator(request):
    return render(request,'mastercreation/operator.html',)
def measurement(request):
    return render(request,'mastercreation/measurement.html',)
def userpermission(request):
    return render(request,'mastercreation/userpermission.html',)
def userscreen(request):
    return render(request,'mastercreation/userscreen.html',)
def machinecreation(request):
    return render(request,'mastercreation/machinecreation.html',)
def shift(request):
    return render(request,'mastercreation/shift.html',)
def paymentterms(request):
    return render(request,'mastercreation/paymentterms.html',)
def consumablecreation(request):
    return render(request,'mastercreation/consumablecreation.html',)
def fabrictype(request):
    return render(request,'mastercreation/fabrictype.html',)
def rollsize(request):
    return render(request,'mastercreation/rollsize.html',)
def gapcreation(request):
    return render(request,'mastercreation/gapcreation.html',)

def jobtypecreation(request):
    return render(request,'mastercreation/jobtypecreation.html',)
def customerstatus(request):
    return render(request,'mastercreation/customerstatus.html',)


def job_no_wise_report(request):
    return render(request,'fusing/job-no-wise-report.html',)
def fusing_operator_wise_report(request):
    return render(request,'fusing/fusing-operator-wise-report.html',)
def fusing_machine_wise_report(request):
    return render(request,'fusing/fusing-machine-wise-report.html',)
def date_wise_report(request):
    return render(request,'fusing/date-wise-report.html',)
def fusing_customer_wise_report(request):
    return render(request,'fusing/fusing-customer-wise-report.html',)
def fusing_production_entry(request):
    return render(request,'fusing/fusing-production-entry.html',)

def printer_customer(request):
    return render(request,'printing/printer_customer.html',)
def printer_data(request):
    return render(request,'printing/printer_data.html',)
def printer_jobwise(request):
    return render(request, 'printing/printer_jobwise.html')

def printer_machine(request):
    return render(request,'printing/printer_machine.html',)
def printer_operator(request):
    return render(request,'printing/printer_operator.html',)
def printer_production(request):
    return render(request,'printing/printer_production.html',)


def inward(request):
    return render(request,'delivery/inward.html',)
def fabric(request):
    return render(request,'delivery/fabric.html',)
def delivery(request):
    return render(request, 'delivery/delivery.html')
def returned(request):
    return render(request,'delivery/returned.html',)
def sticker(request):
    return render(request,'delivery/sticker.html',)





