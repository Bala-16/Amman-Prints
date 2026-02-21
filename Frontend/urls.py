# from django.urls import path
# from . import views

# urlpatterns = [
#     # ✅ Form Page (HTML)
#     path('', views.jobcard_form_view, name='jobcard-form'),
    
#     # ✅ Simple API Endpoints (No DRF - Just JSON Response)
#     path('api/jobcards/', views.get_jobcards, name='get_jobcards'),
#     path('api/jobcards/create/', views.create_jobcard, name='create_jobcard'),
#     path('api/jobcards/<int:pk>/delete/', views.delete_jobcard, name='delete_jobcard'),
#     path('api/jobcards/<int:pk>/edit/', views.edit_jobcard, name='edit_jobcard'),
#     path('api/summary/', views.get_summary, name='get_summary'),
# ]