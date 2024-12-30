import json
from django.db import transaction
from django.shortcuts import render
from requests import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from asgiref.sync import sync_to_async

from .models import *
from dpi.models import *
from dpi.serializers import *
from .serializers import *
from .backends import *
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
        condition["doctor"] = DoctorSerializer(Doctor.objects.get(pk=condition["doctor"]["id"])).data["name"]
        

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
        }, status=204)
    
    except MedicalCondition.DoesNotExist:
        # Return failure response if object doesn't exist
        return JsonResponse({
            "status": "failure",
            "message": "The medical condition page does not exist"
        }, status=404)

    
@api_view(['POST'])
def request_medical_care(request, condition_pk):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response    

    try:
        # Retrieve the MedicalCondition object
        medicalCondition = MedicalCondition.objects.get(pk=condition_pk)

        medicalCare = {}
        if ('description' not in request.data):
            return JsonResponse({
                "status": "failure",
                "message": "please provide the medical care requesting to be done on the patient"
            },status=404)

        medicalCare["description"] = request.data['description']
        if 'title' in request.data:
            medicalCare["title"] = request.data['title']
        if 'priority' in request.data:
            medicalCare["priority"] = request.data['priority']

        medicalCare["patient"] = medicalCondition.patient
        medicalCare["nurse"] = None
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
def view_medical_cares(request, SSN):
    try:
        patient = Patient.objects.get(SSN=SSN)

        caresQuery = Care.objects.filter(patient=patient)

        if "status" in request.GET:
            caresQuery = caresQuery.filter(status = request.GET.get("status"))

        cares = MedCareSerializer(caresQuery, many=True).data

        return JsonResponse({
            "status": "success",
            "data": cares
        },status=200)
        
    except Patient.DoesNotExist:
        return JsonResponse({
            "status": "fail",
            "message": "patient does not exist"
        }, status=404)
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': f'An error occurred: {str(e)}'},
            status =500
            ) 

@api_view(['POST'])
def complete_medical_care(request, pk):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response
    
    try:
        care = Care.objects.get(pk=pk)
        
        if "resume" in request.data:
            care.observation = request.data["resume"]

        care.status = "Completed"

        if "dateCompleted" in request.data:
            care.dateCompleted = request.data["dateCompleted"]
        else:
            care.dateCompleted = datetime.now()

        care.nurse = Nurse.objects.get(pk=request.user["id"])
        
        care.save()
        data = MedCareSerializer(care).data

        return JsonResponse({
            "status": "success",
            "data": data
        },status=200)

    except Care.DoesNotExist:
        return JsonResponse({
            "status": "fail",
            "message": "medical care request does not exist"
        }, status=404)
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': f'An error occurred: {str(e)}'},
            status =500
            ) 


@api_view(['POST'])
def issue_prescription(request, condition_pk):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response
    
    try:
        with transaction.atomic():  # Start a database transaction
            # Retrieve the patient and medical condition
            medical_condition = MedicalCondition.objects.get(pk=condition_pk)
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

        



@api_view(['GET'])
def tester(request):
    auth_response = authenticate(request=request)

    if auth_response:
        return auth_response
    return JsonResponse({
        "status": "success",
        "user": request.user
        },status=200)