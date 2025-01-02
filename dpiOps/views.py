import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime

from .models import *
from dpi.models import *
from dpi.serializers import *
from .serializers import *
from .backends import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import date
from django.db import transaction

 
# Create your views here.


@api_view(['GET'])
def get_medical_history(request,SSN):
    patient = {}
    try:
        patient = Patient.objects.get(SSN=SSN)

    except Patient.DoesNotExist:
        return JsonResponse({
            "status": "failed",
            "message": "Patient does not exist",
        },
        status=404
        )
    medicalHistoryQuery = MedicalCondition.objects.select_related("doctor").filter(patient=patient)

    #check if the results aren't empty
    medicalHistory = {}
    if medicalHistoryQuery:
        medicalHistory = MedCondSerializer(medicalHistoryQuery, many=True).data
    #get the doctor name that treated the conditions
    for condition in medicalHistory:
        condition["doctor"] = DoctorSerializer(Doctor.objects.get(pk=condition["doctor"])).data["name"]
        

    return JsonResponse({
        "status": "success",
        "data": medicalHistory

    },status=200)

  
@api_view(["POST"])
def add_medical_condition(request,patient_pk):
    auth_response = authenticate(request=request)
    if auth_response:
        return auth_response
    try:
        patient = {}
        try:
            patient = Patient.objects.get(pk=patient_pk)

        except Patient.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "message": "Patient does not exist",
            },
            status=404
            )
        if (not request.data.get("reason")):
            return JsonResponse({
                "status": "failure",
                "message": "must provide a reason for the new dpi page"
                },
                status=400)
        
        medicalCondition = MedCondSerializer(MedicalCondition.objects.create(
        reason = request.data.get('reason'),
        patient = patient,
        doctor = Doctor.objects.get(pk=request.user["id"])
        )).data

        return JsonResponse({
            "status": "success",
            "data":
                medicalCondition
        })
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': f'An error occurred: {str(e)}'},
            status =500
            ) 



@api_view(['POST'])    
def edit_medical_condition_page(request, pk):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response
    

    try:
        # Retrieve the MedicalCondition object
        medicalCondition = MedicalCondition.objects.get(pk=pk)
        
        # Check if request data contains values and update accordingly
        if 'resume' in request.data:
            medicalCondition.resume = request.data['resume']
        
        if 'reason' in request.data:
            medicalCondition.reason = request.data['reason']
        


        # Save the object after updating fields
        medicalCondition.save()


        return JsonResponse({
            "status": "success",
            "message": "Medical condition page updated successfully"
        }, status=200)
    
    except MedicalCondition.DoesNotExist:
        # Return failure response if object doesn't exist
        return JsonResponse({
            "status": "failure",
            "message": "The medical condition page does not exist"
        }, status=404)

    
@api_view(['POST'])
def add_medical_care(request, condition_pk):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response    

    try:
        # Retrieve the MedicalCondition object
        medicalCondition = MedicalCondition.objects.get(pk=condition_pk)

        medicalCare = {}
        if ('care' not in request.data) and ('observation' not in request.data):
            return JsonResponse({
                "status": "failure",
                "message": "please provide the medical care done on the patient or an observation"
            },status=404)

        if 'care' in request.data:
            medicalCare["care"] = request.data['care']
        if 'observation' in request.data:
            medicalCare["observation"] = request.data['observation']
        if 'date' in request.data:
            medicalCare["date"] = request.data['care']
        else:
            medicalCare["date"]= datetime.now()

        medicalCare["patient"] = medicalCondition.patient
        medicalCare["nurse"] = Nurse.objects.get(pk=request.user["id"])
        medicalCare["medicalCondition"] = medicalCondition

        careQuery = Care.objects.create(**medicalCare)

        serializedData = MedCareSerializer(careQuery).data

        return JsonResponse({
            "status": "success",
            "data": serializedData
        },status = 200)


        

    except MedicalCondition.DoesNotExist:
        # Return failure response if object doesn't exist
        return JsonResponse({
            "status": "failure",
            "message": "The medical condition page does not exist"
        }, status=404)
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': f'An error occurred: {str(e)}'},
            status =500
            ) 
    




@api_view(['GET'])
def tester(request):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response
    return JsonResponse({
        "status": "success",
        "user": request.user
        },status=200)





class RequestTest(APIView):
    def post(self, request):
        try:
            data = request.data
            patient_NSS = data.get('patient_NSS')
            role = data.get('test_to')
            dpi_id = data.get('dpi_id')

            # Check if patient exists
            try:
                patient = Patient.objects.get(SSN=patient_NSS)
            except Patient.DoesNotExist:
                return JsonResponse({
                    "status": "failed",
                    "message": "Patient does not exist",
                }, status=404)

            # Check if medical condition (DPI) exists
            try:
                medicalcondition = MedicalCondition.objects.get(id=dpi_id)
            except MedicalCondition.DoesNotExist:
                return JsonResponse({
                    "status": "failed",
                    "message": "DPI does not exist",
                }, status=404)

            # Create the appropriate test based on the 'role' (radiologist or laborantin)
            if role == 'radiologist':
                test = Radio_test.objects.create(
                    status='pending',  
                    patient=patient,
                    description=data.get('description'),
                    title=data.get('title'),
                    priorite=data.get('priorite'),
                    medicalCondition=medicalcondition,
                )
                response_data = {
                    "status": "success",
                    "message": "Radiology test created successfully",
                    "test_id": test.id,
                    "test_type": "radiologist",
                }

            elif role == 'laborantin':
                test = Baio_test.objects.create(
                    status='pending',  # Corrected the typo here
                    patient=patient,
                    description=data.get('description'),
                    title=data.get('title'),
                    priorite=data.get('priorite'),
                    medicalCondition=medicalcondition,
                )
                response_data = {
                    "status": "success",
                    "message": "Laboratory test created successfully",
                    "test_id": test.id,
                    "test_type": "laborantin",
                }
            elif role == "nurse":
                test = Nurse_test.objects.create(
                    status='pending',  # Corrected the typo here
                    patient=patient,
                    description=data.get('description'),
                    title=data.get('title'),
                    priorite=data.get('priorite'),
                    medicalCondition=medicalcondition,
                )
                response_data = {
                    "status": "success",
                    "message": "Laboratory test created successfully",
                    "test_id": test.id,
                    "test_type": "laborantin",
                }                
            else:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid test type provided. Must be 'radiologist' or 'laborantin'.",
                }, status=400)


            # Return a successful response
            return JsonResponse(response_data, status=201)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        # Return an error for GET requests
        return Response({
            'status': 'error',
            'message': 'Only POST method is allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



class BaioTest(APIView):
    def put(self, request, pk):
        try:
            baio_test = Baio_test.objects.get(pk=pk)
        except Baio_test.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Baio_test not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        baio_test.status = 'completed'
        baio_test.conductionDate=date.today()
        serializer = BaioTestSerializer(baio_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            })
        else:
            return Response({
                "status": "failed",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



class RadioTest(APIView):
    def put(self, request, pk):
        try:
            radio_test = Radio_test.objects.get(pk=pk)
        except Radio_test.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Radio_test not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        radio_test.status = 'completed'
        radio_test.conductionDate=date.today()
        serializer = RadioTestSerializer(radio_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "status": "success",
                "message": "Radio_test updated and status set to 'completed'",
                "data": serializer.data
            })
        else:
            return Response({
                "status": "failed",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        



class NurseTest(APIView):
    def put(self, request, pk):
        try:
            nurse_test = Nurse_test.objects.get(pk=pk)
        except Nurse_test.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Nurse_test not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        nurse_test.status = 'completed'
        nurse_test.conductionDate=date.today()
        serializer = NurseTestSerializer(nurse_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "status": "success",
                "message": "Nurse_test updated and status set to 'completed'",
                "data": serializer.data
            })
        else:
            return Response({
                "status": "failed",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class GetAllBaioTests(APIView):
    def get(self, request):
        baio_tests = Baio_test.objects.all()
        baio_tests_data = BaioTestSerializer(baio_tests, many=True).data
        patiens = [test.patient for test in baio_tests]
        return Response({
            "status": "success",
            "data": baio_tests_data,
            "patients": PatientSerializer(patiens,many=True).data,
        })
    

class GetBaioTestById(APIView):
    def get(self, request, pk):
        try:
            baio_test = Baio_test.objects.get(id=pk)
            baio_test_data = BaioTestSerializer(baio_test).data
            return Response({
                "status": "success",
                "data": baio_test_data
            })
        except Baio_test.DoesNotExist:
            raise NotFound(detail="Baio_test not found")



class GetAllRadioTests(APIView):
    def get(self, request):
        radio_tests = Radio_test.objects.all()
        radio_tests_data = RadioTestSerializer(radio_tests, many=True).data
        patiens = [test.patient for test in radio_tests]

        return Response({
            "status": "success",
            "data": radio_tests_data,
            "patients": PatientSerializer(patiens,many=True).data,
        })
    

class GetAllNurseTests(APIView):
    def get(self, request):
        nurse_tests = Nurse_test.objects.all()
        patiens = [test.patient for test in nurse_tests]

        nurse_tests_data = NurseTestSerializer(nurse_tests, many=True).data
        
        return Response({
            "status": "success",
            "data": nurse_tests_data,
            "patients": PatientSerializer(patiens,many=True).data,
        })
    



class GetRadioTestById(APIView):
    def get(self, request, pk):
        try:
            # Retrieve the specific Radio_test by ID
            radio_test = Radio_test.objects.get(id=pk)
            radio_test_data = RadioTestSerializer(radio_test).data
            return Response({
                "status": "success",
                "data": radio_test_data
            })
        except Radio_test.DoesNotExist:
            raise NotFound(detail="Radio_test not found")





class TestHistory(APIView):
    def get(self, request, medical_condition_id):
        baio_tests = Baio_test.objects.filter(medicalCondition_id=medical_condition_id)
        radio_tests = Radio_test.objects.filter(medicalCondition_id=medical_condition_id)
        nurse_tests = Nurse_test.objects.filter(medicalCondition_id=medical_condition_id)
        baio_tests_data = BaioTestSerializer(baio_tests, many=True).data
        radio_tests_data = RadioTestSerializer(radio_tests, many=True).data
        nurse_tests = NurseTestSerializer(nurse_tests, many=True).data

        # Combine both test types
        combined_data = {
            "baio_tests": baio_tests_data,
            "radio_tests": radio_tests_data,
            "nurse_tests": nurse_tests,
        }

        if not combined_data["baio_tests"] and not combined_data["radio_tests"]:
            return Response({
                "status": "failed",
                "message": "No tests found for this medical condition"
            }, status=404)

        return Response({
            "status": "success",
            "data": combined_data
        })





class GetTestByIdAndType(APIView):
    def get(self, request):
        test_id = request.query_params.get('id')
        test_type = request.query_params.get('type')
        if not test_id or not test_type:
            return Response({
                "status": "failed",
                "message": "Both 'id' and 'type' query parameters are required."
            }, status=400)
        if test_type not in ['baio_test', 'radio_test']:
            return Response({
                "status": "failed",
                "message": "Invalid test type. Must be 'baio_test' or 'radio_test'."
            }, status=400)
        if test_type == 'baio_test':
            try:
                test = Baio_test.objects.get(id=test_id)
            except Baio_test.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "Baio_test not found"
                }, status=404)
            test_data = BaioTestSerializer(test).data
        elif test_type == 'radio_test':
            try:
                test = Radio_test.objects.get(id=test_id)
            except Radio_test.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "Radio_test not found"
                }, status=404)
            test_data = RadioTestSerializer(test).data

        return Response({
            "status": "success",
            "data": test_data
        })




@api_view(['POST'])
def issue_prescription(request, condition_pk):
    auth_response = authenticate(request=request)
    if auth_response:
        return auth_response
    
    try:
        with transaction.atomic():  # Start a database transaction
            # Retrieve the patient and medical condition
            medical_condition = MedicalCondition.objects.get(pk=condition_pk)
            medical_condition.lastedFor = date.today()
            medical_condition.save()
             
            patient = medical_condition.patient
            doctor = Doctor.objects.get(pk=request.user["id"])  # Assuming user is a doctor

            # Extract prescription data
            prescription_data = {
                "notes": request.data.get("notes", ""),
                "patient": patient,
                "doctor": doctor,
                "medicalCondition": medical_condition,
            }

            # Create the prescription
            prescription = Prescription.objects.create(**prescription_data)

            # Validate and add prescription entries
            entries = request.data.get("entries", [])
            if not entries:
                raise ValueError("At least one prescription entry is required.")

            for entry in entries:
                required_fields = ["name", "dosage", "frequency", "duration", "instructions"]
                missing_fields = [field for field in required_fields if not entry.get(field)]

                if missing_fields:
                    raise ValueError(f"Missing fields in entry: {', '.join(missing_fields)}")

                PrescriptionEntry.objects.create(
                    name=entry["name"],
                    dosage=entry["dosage"],
                    frequency=entry["frequency"],
                    duration=entry["duration"],
                    instructions=entry["instructions"],
                    prescription=prescription,
                )
            

            return JsonResponse({
                "status": "success",
                "message": "Prescription added successfully",
                "prescription": {
                    "id": prescription.id,
                    "issueDate": prescription.issueDate,
                    "validationDate": prescription.validationDate,
                    "status": prescription.status,
                    "notes": prescription.notes,
                    "entries": [
                        {
                            "name": entry["name"],
                            "dosage": entry["dosage"],
                            "frequency": entry["frequency"],
                            "duration": entry["duration"],
                            "instructions": entry["instructions"],
                        } for entry in entries
                    ]
                }
            }, status=201)

    except Patient.DoesNotExist:
        return JsonResponse({
            "status": "failure",
            "message": "Patient not found"
        }, status=404)

    except MedicalCondition.DoesNotExist:
        return JsonResponse({
            "status": "failure",
            "message": "Medical condition not found"
        }, status=404)

    except Doctor.DoesNotExist:
        return JsonResponse({
            "status": "failure",
            "message": "Doctor not found"
        }, status=404)

    except ValueError as e:
        return JsonResponse({
            "status": "failure",
            "message": str(e)
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)
    


@api_view(['GET'])
def view_prescriptions(request):
    try:
        params = request.GET
        query = {}
        
        if "condition_pk" in params:
            query = MedicalCondition.objects.get(pk=params.get("condition_pk")).prescriptions
            
        elif "patient_SSN" in params:
            query = Patient.objects.get(SSN=params.get("patient_SSN")).prescriptions
        
        else:
            query = Prescription.objects

        if "status" in params:
            query = Prescription.objects.filter(status=params.get("status"))

        # Fetch prescriptions 
        prescriptions = query.prefetch_related('entries').all()

        # Serialize the prescriptions
        serializer = PrescriptionSerializer(prescriptions, many=True)

        return JsonResponse({
            "status": "success",
            "data": serializer.data
        }, status=200)

    except MedicalCondition.DoesNotExist:
        return JsonResponse({
            "status": "failure",
            "message": "Medical condition not found"
        }, status=404)
    except Patient.DoesNotExist:
        return JsonResponse({
            "status": "failure",
            "message": "Patient not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)
    
@api_view(['POST'])
def update_prescription_status(request, prescription_pk):

    try:
        #fetch the prescription
        prescription = Prescription.objects.get(pk=prescription_pk)

        if "status" in request.data:
            prescription.status = request.data.get("status")
        else:
            raise(ValueError("please indicated whether the prescription is Validated or Failed"))
        
        prescription.validationDate = date.today()

        #validation
        prescription.full_clean()

        prescription.save()

        return JsonResponse({
            "status": "success",
            "data": PrescriptionSerializer(prescription).data
        },status=200)
    
    except Prescription.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "prescription does not exist"
        },status =404)
    except ValueError as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        },status = 400)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        },status = 500)

        
