from django.urls import path
from . import views

urlpatterns = [
    path('', views.nav, name='home'),   # ← THIS WAS MISSING
    path('nav/', views.nav, name='nav'),
    path('jobcard/customer_report/', views.customer_report, name='customer_report'),
    path('jobcard/quotation/', views.quotation, name='quotation'),
    path('jobcard/designer_report/', views.designer_report, name='designer_report'),
    path('jobcard/quotation_form/', views.quotation_form, name='quotation_form'),
   path('jobcard/job_creation/', views.job_creation, name='job_creation'),
    path('jobcard/job_list/', views.job_list, name='job_list'),


    path('process_report/', views.process_report, name='process_report'),
    path('quotation_customer/', views.quotation_customer, name='quotation_customer'),
  
 
    
    path('printing/', views.printing, name='printing'),
    path('consumable/', views.consumable, name='consumable'),
    path('accounts/', views.accounts, name='accounts'),
    path('delivery/', views.delivery, name='delivery'),
    path('dashboard/', views.nav, name='dashboard'),
  
    path('customer_report/', views.customer_report, name='customer_report'),

    path('mastercreation/operator/', views.operator, name='operator'),
    path('mastercreation/measurement/', views.measurement, name='measurement'),
    path('mastercreation/userpermission/', views.userpermission, name='userpermission'),
    path('mastercreation/userscreen/', views.userscreen, name='userscreen'),
    path('mastercreation/machinecreation/', views.machinecreation, name='machinecreation'),
    path('mastercreation/shift/', views.shift, name='shift'),
    path('mastercreation/paymentterms/', views.paymentterms, name='paymentterms'),
    path('mastercreation/consumablecreation/', views.consumablecreation, name='consumablecreation'),
    path('mastercreation/fabrictype/', views.fabrictype, name='fabrictype'),
    path('mastercreation/rollsize/', views.rollsize, name='rollsize'),
    path('mastercreation/gapcreation/', views.gapcreation, name='gapcreation'),
    path('mastercreation/jobtypecreation/', views.jobtypecreation, name='jobtypecreation'),
    path('mastercreation/customerstatus/', views.customerstatus, name='customerstatus'),
    path('mastercreation/company_creation/', views.company_creation, name='company_creation'),
    path('mastercreation/party_creation/', views.party_creation, name='party_creation'),
    path('mastercreation/user_type_creation/', views.user_type_creation, name='user_type_creation'),

    path('fusing/', views.fusing, name='fusing'), 
    path('fusing/job-no-wise-report/', views.job_no_wise_report, name='job_no_wise_report'),
    path('fusing/fusing-operator-wise-report/', views.fusing_operator_wise_report, name='fusing_operator_wise_report'),
    path('fusing/fusing-machine-wise-report/', views.fusing_machine_wise_report, name='fusing_machine_wise_report'),
    path('fusing/date-wise-report/', views.date_wise_report, name='date_wise_report'),
    path('fusing/fusing-customer-wise-report/', views.fusing_customer_wise_report, name='fusing_customer_wise_report'),
    path('fusing/fusing-production-entry/', views.fusing_production_entry, name='fusing_production_entry'),


    path('printing/printer_customer/',views.printer_customer, name='printer_customer'),
    path('printing/printer_data/',views.printer_data, name='printer_data'),
    path('printing/printer_jobwise/',views.printer_jobwise,name='printer_jobwise'),
    path('printing/printer_machine/',views.printer_machine, name='printer_machine'),
    path('printing/printer_operator/',views.printer_operator, name='printer_operator'), 
    path('printing/printer_production/',views.printer_production, name='printer_production'),
]
