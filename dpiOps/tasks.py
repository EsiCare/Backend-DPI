import random
import requests
from celery import shared_task
from .models import Prescription

@shared_task
def validate_random_prescription():
    # Pick a random prescription
    prescriptions = list(Prescription.objects.filter(status="Pending"))
    if not prescriptions:
        return "No pending prescriptions to validate."

    prescription = random.choice(prescriptions)

    # Send the prescription details to the external server
    external_server_url = "https://localhost:5000/api/validate"
    payload = {
        "id": prescription.id,
        "issueDate": str(prescription.issueDate),
        "notes": prescription.notes,
        "patient": prescription.patient.id,
    }

    try:
        response = requests.post(external_server_url, json=payload)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("result") == "true":
            prescription.status = "Validated"
        else:
            prescription.status = "Failed"

        prescription.save()
        print()
        return f"{prescription.__str__()} updated to {prescription.status}."
    
    except requests.RequestException as e:
        return f"Failed to validate {prescription.__str__()}: {str(e)}"
