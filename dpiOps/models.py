from django.db import models
from dpi.models import *
# Create your models here.

class   MedicalCondition (models.Model):
    date=models.DateField(auto_now_add=True)
    lastedFor=models.CharField(max_length=30,blank=True)
    reason= models.CharField(max_length=100)
    resume= models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=50, default="In Treatment")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Condition for {self.patient.user.username}"

class Prescription (models.Model):
    issueDate = models.DateField(auto_now_add=True)
    validationDate=models.DateField(blank=True, null=True)
    status=models.CharField(max_length=50, default="Pending")
    notes=models.CharField(max_length=300, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    medicalCondition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE, related_name="prescriptions")
    
    def __str__(self):
        return f"Prescription for {self.patient.user.username}"

class PrescriptionEntry(models.Model):
    name = models.CharField(max_length=50, blank=True) 
    dosage = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(max_length=50, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    instructions = models.CharField(max_length=100, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="entries")

class Care (models.Model):
    title = models.CharField(max_length=50, default="Medical Care")
    description = models.CharField(max_length=500, blank=True)
    observation = models.CharField(max_length=500, blank=True)
    priority = models.CharField(max_length=50, default="Normal")
    status = models.CharField(max_length=30, default="Pending")
    dateIssued = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(blank=True, null=True)
    medicalCondition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE, related_name="cares")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.OneToOneField(Nurse, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Medical Care for {self.patient.user.username}"


# Test model (now with type differentiation)
class Test(models.Model):
    TEST_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed')
    )
    issueDate = models.DateField(auto_now_add=True)
    conductionDate = models.DateField(blank=True)
    status = models.CharField(max_length=10, choices = TEST_STATUS)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.get_type_display()} test for {self.patient.user.username}"
    
    class Meta:
        ordering = ['-issueDate']
        abstract = True  # This makes it an abstract model



# Bloodwork model (if still needed)
class Bloodwork(Test):
    medicalCondition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE, related_name="bloodworks")
    results = models.TextField()


# Scan model (if still needed)
class Scan(Test):
    medicalCondition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE, related_name="tests")
    image = models.ImageField(upload_to='examinations/', blank=True, null=True)