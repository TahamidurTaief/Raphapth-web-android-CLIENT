from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.conf import settings

# Create your models here.





class CustomUser(AbstractUser):
    USER = (
        ('0', 'SUPERADMIN'),
        ('1', 'HOC'),
        ('2', 'DOCTOR'),
        ('3', 'PATIENT'),       
    )

    user_type = models.CharField(choices=USER, max_length=10, default='1')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Custom related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username
   





class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    helpline = models.CharField(max_length=20, default='Not Available', null=True, blank=True)
    ccmd = models.BooleanField(default=False)
    vmmc = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# departments = [
#     ('Cardiologist', 'Cardiologist'),
#     ('Dermatologists', 'Dermatologists'),
#     ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
#     ('Allergists/Immunologists', 'Allergists/Immunologists'),
#     ('Anesthesiologists', 'Anesthesiologists'),
#     ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
# ]

class Hoc(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.clinic)


class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    status = models.BooleanField(default=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)
    id_no = models.CharField(max_length=100, null=True, default="")
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    home_distance = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + self.user.first_name


class Appointment(models.Model):
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default="")
    doctorId = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, default="")
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(null=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PatientHospitalized(models.Model):
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)

    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.quantity > 0


class OrderMedicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255, default="", blank=True, null=True)
    address = models.TextField(default="", blank=True, null=True)
    phone_number = models.CharField(max_length=20, default="", blank=True, null=True)
    payment_method = models.CharField(max_length=10, default="", blank=True, null=True)
    transaction_id = models.CharField(max_length=50, default="", blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order_quantity = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.medicine.name}"


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class OrderTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255, default="", blank=True, null=True)
    address = models.TextField(default="", blank=True, null=True)
    phone_number = models.CharField(max_length=20, default="", blank=True, null=True)
    payment_method = models.CharField(max_length=10, default="", blank=True, null=True)
    transaction_id = models.CharField(max_length=50, default="", blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.test.name}"




class TestReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test = models.ManyToManyField(Test)
    result = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test Report for {self.patient.user.username} by {self.doctor.user.username}"




# WEBSITE START
# ====================================

class Web_About_us(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    


class Web_Contact_us(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, default="0000000000", blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
    


class Web_Latest_Articles(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    specialist = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Web_Specialist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name