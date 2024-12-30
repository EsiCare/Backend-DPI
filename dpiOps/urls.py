
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
    path("api/prescriptions", view_prescriptions, name="view_prescriptions"),
    path("api/prescriptions/update/<int:prescription_pk>", update_prescription_status, name="update_prescription_status"),
    
    path("api/tester", tester, name="tester")




    path('api/request-test/', RequestTest.as_view(), name='request-test'),
    path('api/baio_test/<int:pk>/', BaioTest.as_view(), name='edit-baio-test'),
    path('api/radio_test/<int:pk>/', RadioTest.as_view(), name='edit-radio-test'),
    path('api/baio-tests/<int:pk>/', GetAllBaioTests.as_view(), name='get_all_baio_tests'),
    path('api/radio-tests/<int:pk>/', GetAllRadioTests.as_view(), name='get_all_radio_tests'),
    path('api/baio-test/<int:pk>/', GetBaioTestById.as_view(), name='get_baio_test_by_id'),
    path('api/radio-test/<int:pk>/', GetRadioTestById.as_view(), name='get_radio_test_by_id'),
    path('api/testhistory/<int:medical_condition_id>/', TestHistory.as_view(), name='testhistory'),
    path('api/testhistory/get-test/', GetTestByIdAndType.as_view(), name='get_test_by_query'),


]