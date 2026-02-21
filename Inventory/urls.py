from django.urls import path
from . import views
from .views import party_list, party_create

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('nav/', views.nav, name='nav'),

    path('jobcard_form_view/', views.jobcard_form_view, name='jobcard_form'),
    
    # ✅ API Endpoints
    path('api/jobcards/', views.get_jobcards, name='get_jobcards'),
    path('api/jobcards/create/', views.create_jobcard, name='create_jobcard'),
    path('api/jobcards/<int:pk>/delete/', views.delete_jobcard, name='delete_jobcard'),
    path('api/jobcards/<int:pk>/edit/', views.edit_jobcard, name='edit_jobcard'),
    path('api/summary/', views.get_summary, name='get_summary'),
    
    # ✅ NEW - Jobcard Process Report API
    path('api/jobcard/<str:jobcard_no>/process-details/', views.get_jobcard_process_details, name='get_jobcard_process_details'),

    path("party/", party_list, name="party_list"),
    path("party/new/", party_create, name="party_create"),

    path('jobcard/customer_report/', views.customer_report, name='customer_report'),
    path('jobcard/designer_report/', views.designer_report, name='designer_report'),
    path('jobcard/quotation_list/', views.quotation_list, name="quotation_list"),
    path("jobcard/quotation_form/", views.quotation_form, name="quotation_form"),
    path("quotation/<int:pk>/view/", views.quotation_view, name="quotation_view"),
    path("quotation/<int:pk>/edit/", views.quotation_edit, name="quotation_edit"),
    path("quotation/<int:pk>/delete/", views.quotation_delete, name="quotation_delete"),
    
    path('jobcard/quotation_customer_report/', views.quotation_customer_report, name='quotation_customer_report'),
  
    path('process_report/', views.process_report, name='process_report'),
  
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
    path('mastercreation/user_name/', views.user_name, name='user_name'),

    path('fusing/', views.fusing, name='fusing'), 
    path('fusing/job-no-wise-report/', views.job_no_wise_report, name='job_no_wise_report'),
    path('fusing/fusing-operator-wise-report/', views.fusing_operator_wise_report, name='fusing_operator_wise_report'),
    path('fusing/fusing-machine-wise-report/', views.fusing_machine_wise_report, name='fusing_machine_wise_report'),
    path('fusing/date-wise-report/', views.date_wise_report, name='date_wise_report'),
    path('fusing/fusing-customer-wise-report/', views.fusing_customer_wise_report, name='fusing_customer_wise_report'),
    path('fusing/fusing-production-entry/', views.fusing_production_entry, name='fusing_production_entry'),

    path('printing/printer_customer/', views.printer_customer, name='printer_customer'),
    path('printing/printer_data/', views.printer_data, name='printer_data'),
    path('printing/printer_jobwise/', views.printer_jobwise, name='printer_jobwise'),
    path('printing/printer_machine/', views.printer_machine, name='printer_machine'),
    path('printing/printer_operator/', views.printer_operator, name='printer_operator'), 
    path('printing/printer_production/', views.printer_production, name='printer_production'),
    
    path('consumable/ink_entry/', views.ink_entry, name='ink_entry'),
    path('consumable/return_form/', views.return_form, name='return_form'),
    path('consumable/stock_report/', views.stock_report, name='stock_report'),
   
    path('delivery/deli/', views.delivery, name='deli'),
    path('delivery/fabric/', views.fabric, name='fabric'),
    path('delivery/inward/', views.inward, name='inward'),
    path('delivery/return/', views.returned, name='return'),
    path('delivery/sticker/', views.sticker, name='sticker'),   
]