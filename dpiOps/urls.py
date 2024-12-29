from django.urls import path
from .views import *

urlpatterns = [
    path("api/medicalHistory/<str:SSN>", get_medical_history, name="get_medical_history"),
    path("api/medicalHistory/add/<int:patient_pk>", add_medical_condition, name="add_medical_condition"),
    path("api/medicalHistory/edit/<int:pk>", edit_medical_condition_page, name="edit_medical_condition_page"),
    # path("api/medicalConditions/<int:pk>")

    path("api/medicalCares/add/<int:condition_pk>",request_medical_care, name="add_medical_care"),
    path("api/medicalCares/<int:SSN>", view_medical_cares, name="view_medical_cares"),
    path("api/medicalCares/complete/<int:pk>", complete_medical_care, name="complete_medical_care"),

    path("api/prescriptions/add/<int:condition_pk>", issue_prescription, name="issue_prescription"),
    path("api/prescriptions/<int:condition_pk>", view_prescriptions, name="view_prescriptions"),
    
    path("api/tester", tester, name="tester")
]