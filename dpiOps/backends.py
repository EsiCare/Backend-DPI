from datetime import time
import jwt
from django.conf import settings
from django.http import JsonResponse
import asyncio
import aiohttp
from django.http import JsonResponse

from dpi.models import *
from dpi.serializers import *
from .models import *

# def authenticate(request):
#     user = {}
#     user["id"] = 5
#     user["name"] = "Dr.Doktor"
#     user["role"] = "doctor"


#     request.user = user




def authenticate(request):
    """
    Decodes the JWT token from the Authorization header and appends user info to request.
    """
    auth_header = request.headers.get('Authorization', None)
    role_model_dict = {
        "radiologist": Radiologist,
        "patient": Patient,
        "doctor": Doctor,
        "administrative": Administrative,
        "laborantin": Laborantin,
        "nurse": Nurse
    }
    role_serializer_dict = {
        "radiologist": RadiologistSerializer,
        "patient": PatientSerializer,
        "doctor": DoctorSerializer,
        "administrative": AdministrativeSerializer,
        "laborantin": LaborantinSerializer,
        "nurse": NurseSerializer
    }
    if auth_header:
        try:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Extract the token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                
                # Append user info to the request object
                userQuery = role_model_dict[payload.get("role")].objects.get(pk=payload.get("actor_id"))
                user = role_serializer_dict[payload.get("role")](userQuery).data

                request.user = user
                
                

            else:
                return JsonResponse({"error": "Invalid authorization header"}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
    else:
        return JsonResponse({"error": "Authorization header not found"}, status=401)

    return None


# Asynchronous function to send HTTP request
async def validate_prescription(prescription_id):
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(15)
        try:
            async with session.post('https://localhost:5000/api/validate') as response:
                if response.status == 200:
                    json_response = await response.json()
                    if json_response.get("result") == "true":
                        # Update prescription status to 'validated'
                        prescription = await Prescription.objects.aget(id=prescription_id)
                        prescription.status = "validated"
                        await prescription.asave()
                    else:
                        # Update prescription status to 'failed'
                        prescription = await Prescription.objects.aget(id=prescription_id)
                        prescription.status = "failed"
                        await prescription.asave()
            print(f"{prescription.__str__()} status changed to {prescription.status}")
        except Exception as e:
            print(f"Error while sending prescription to external server: {e}")
