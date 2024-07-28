
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse



@login_required(login_url='/login/')
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user.id)
    doctor_name = doctor.user.first_name + ' ' + doctor.user.last_name
    clinic = doctor.clinic

    doctor_count = Doctor.objects.filter(clinic=clinic).count()
    patient_count = Patient.objects.filter(clinic=clinic).count()
    clinic_count = Clinic.objects.count()
    ccmd_clinic_count = Clinic.objects.filter(ccmd=True).count()

    # Fetch recent approved patients
    recent_approved_patients = Patient.objects.filter(clinic=clinic, status=True).order_by('-admitDate')[:5]

    # Fetch recent appointments
    recent_appointments = Appointment.objects.filter(clinic=clinic).order_by('-appointmentDate')[:5]

    context = {
        'doctor': doctor,
        'doctor_name': doctor_name,
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'clinic_count': clinic_count,
        'ccmd_clinic_count': ccmd_clinic_count,
        'recent_approved_patients': recent_approved_patients,
        'recent_appointments': recent_appointments,
    }

    return render(request, 'doctor/doctor_dashboard.html', context)



@login_required(login_url='/login/')
def doctor_view_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)  # Get the logged-in doctor
    appointments = Appointment.objects.filter(doctorId=doctor, status=True)
    context = {
        'appointments': appointments,
        'doctor': doctor,
    }
    return render(request, 'doctor/doctor_view_appointment.html', context)



@login_required(login_url='/login/')
def doctor_delete_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)  # Get the logged-in doctor
    appointments = Appointment.objects.filter(doctorId=doctor, status=True)
    context = {
        'appointments': appointments,
        'doctor': doctor,
    }
    return render(request, 'doctor/doctor_delete_appointment.html', context)




@login_required(login_url='/login/')
def delete_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.delete()
    messages.success(request, 'Appointment deleted successfully')
    return redirect(reverse('doctor_delete_appointment_view'))







