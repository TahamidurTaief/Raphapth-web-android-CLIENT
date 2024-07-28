from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q





def is_patient(user):
    return user.is_authenticated and hasattr(user, '2')




@login_required(login_url='/login/')
def patientDashboard(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)  # Assuming the request.user is the admin
        clinic = patient.clinic  # Assuming each admin is associated with a single clinic

        doctor_count = Doctor.objects.filter(clinic=clinic).count()
        patient_count = Patient.objects.filter(clinic=clinic).count()
        clinic_count = Clinic.objects.all().count()
        test_report_count = TestReport.objects.filter(patient = patient).count()
        patient = Patient.objects.get(user=request.user.id)
        patient_name = patient.user.first_name + ' ' + patient.user.last_name

        recent_appointments = Appointment.objects.filter(patientId=patient).order_by('-appointmentDate')[:5]
        recent_test_results = TestReport.objects.filter(patient=patient).order_by('-date')[:5]
        context = {
            'patient': patient,
            'patient_name': patient_name,
            'doctor_count': doctor_count,
            'patient_count': patient_count,
            'clinic_count': clinic_count,
            'test_report_count': test_report_count,
            'recent_appointments': recent_appointments,
            'recent_test_results': recent_test_results,
        }
    else:
        return redirect('login')
    
    return render(request, 'patient/patient_dashboard.html', context)





@login_required(login_url='login')
# @user_passes_test(is_patient)
def patient_appointment_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    patient = get_object_or_404(Patient, user_id=request.user.id)
    appointments = Appointment.objects.filter(patientId=patient.id)
    return render(request, 'patient/patient_appointment.html', {'patient': patient, 'appointments': appointments})





@login_required(login_url='/login/')
def patient_book_appointment_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    

    patient = get_object_or_404(Patient, user_id=request.user.id)
    message = None
    context = {'patient': patient, 'message': message}
    
    if request.method == 'POST':
        description = request.POST.get('description')
        doctor_id = request.POST.get('doctorId')
        date = request.POST.get('appointmentDate')
        
        if description and doctor_id:
            doctor = get_object_or_404(Doctor, user_id=doctor_id)
            
            appointment = Appointment(
                description=description,
                doctorId=doctor,
                patientId=patient,
                doctorName=doctor.user.first_name,
                patientName=request.user.first_name,
                appointmentDate = date,
                status=False,
                clinic=doctor.clinic
            )
            appointment.save()
            
            return HttpResponseRedirect(reverse('patient_appointment_view'))
        
    patient = get_object_or_404(Patient, user=request.user)
    clinic = patient.clinic    
    doctors = Doctor.objects.filter(status=True, clinic=clinic)
    context['doctors'] = doctors
    return render(request, 'patient/patient_book_appointment.html', context)






@login_required(login_url='login')
def patient_view_doctor_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    clinic = patient.clinic 
    doctors = Doctor.objects.filter(status=True, clinic=clinic)
    return render(request, 'patient/patient_view_doctor.html', {'doctors': doctors})




@login_required(login_url='login')
def search_doctor_view(request):
    patient = get_object_or_404(Patient, user_id=request.user.id)
    query = request.GET.get('query', '')
    doctors = Doctor.objects.filter(
        status=True
    ).filter(
        Q(user__first_name__icontains=query) | 
        Q(user__last_name__icontains=query) |
        Q(clinic__name__icontains=query)  # assuming clinic has a name field
    )
    return render(request, 'patient/patient_view_doctor.html', {'doctors': doctors, 'patient': patient})




@login_required(login_url='login')
def medicine_shop_view(request):
    medicines = Medicine.objects.all()
    return render(request, 'patient/medicine_shop.html', {'medicines': medicines})



@login_required(login_url='login')
def purchase_medicine_view(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'patient/purchase_medicine.html', {'medicine': medicine})



@login_required(login_url='login')
def process_order_view(request, pk):
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, pk=pk)
        patient_name = request.POST.get('patient_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        order_quantity = int(request.POST.get('order_quantity', 1))

        if medicine.quantity < order_quantity:
            messages.error(request, 'Insufficient stock available.')
            return redirect('purchase_medicine', pk=pk)

        OrderMedicine.objects.create(
            medicine=medicine,
            patient_name=patient_name,
            address=address,
            phone_number=phone_number,
            payment_method=payment_method,
            transaction_id=transaction_id,
            order_quantity=order_quantity
        )

        medicine.quantity -= order_quantity
        medicine.save()

        messages.success(request, 'Order placed successfully!')
        return redirect('medicine_shop')

    return redirect('medicine_shop')




@login_required
def test_view(request):
    tests = Test.objects.all()
    return render(request, 'patient/test_view.html', {'tests': tests})






@login_required(login_url='login')
def patient_test_reports_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    test_reports = TestReport.objects.filter(patient=patient)
    return render(request, 'patient/patient_test_reports.html', {'test_reports': test_reports})