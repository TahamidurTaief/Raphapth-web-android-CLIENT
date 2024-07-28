from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.template.loader import get_template
from html import escape
from xhtml2pdf import pisa
import io
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
# Create your views here.









@login_required(login_url='/login/')
def AdminDashboard(request):


    admin = Hoc.objects.get(user=request.user)
    clinic = admin.clinic

    # Fetch counts
    doctor_count = Doctor.objects.filter(clinic=clinic).count()
    patient_count = Patient.objects.filter(clinic=clinic).count()
    clinic_count = Clinic.objects.all().count()
    ccmd_clinic_count = Clinic.objects.filter(ccmd=True).count()  # Update this line based on your model

    # Fetch recent appointments
    recent_appointments = Appointment.objects.filter(clinic=clinic).order_by('-appointmentDate')[:5]
    recent_approved_patients = Patient.objects.filter(clinic=clinic, status=True)

    # Aggregate patient data by year
    male_patients = Patient.objects.filter(gender='M').count()
    female_patients = Patient.objects.filter(gender='F').count()
    other_patients = Patient.objects.filter(gender='O').count()

    # print(f"\n\n{male_patients}\n{female_patients}\n\n")
    context = {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'clinic_count': clinic_count,
        'ccmd_clinic_count': ccmd_clinic_count,
        'clinic_name': clinic.name,
        'recent_appointments': recent_appointments,
        'recent_approved_patients': recent_approved_patients,
        'male_patients': male_patients,
        'female_patients': female_patients,
        'other_patients':other_patients,
    }
    return render(request, 'admin/admin_dashboard.html', context)








@login_required(login_url='/login/')
def addDoctor(request):
    return render(request, 'admin/add_doctor.html')



@login_required(login_url='/login/')
@login_required(login_url='/login/')
def saveDoctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        profile_pic = request.FILES.get('profile_pic')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            try:
                clinic = request.user.hoc.clinic
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )
                doctor = Doctor(
                    user=user,
                    gender=gender,
                    mobile=mobile,
                    address=address,
                    profile_pic=profile_pic,
                    clinic=clinic
                )
                doctor.save()
                messages.success(request, 'Doctor registered successfully')
                return redirect('viewDoctor')
            except Exception as e:
                messages.error(request, 'Error: ' + str(e))
    return render(request, 'signup.html')






@login_required(login_url='/login/')
def deleteDoctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    

    doctor.user.delete()  # Delete the associated User
    doctor.delete()  # Delete the Doctor instance
    messages.success(request, 'Doctor deleted successfully')
    return redirect('viewDoctor')

    # return redirect('viewDoctor')  # Redirect if the request method is not POST




@login_required(login_url='/login/')
def editDoctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        profile_pic = request.FILES.get('profile_pic')

        try:
            # Update user details
            doctor.user.first_name = first_name
            doctor.user.last_name = last_name
            doctor.user.username = username
            doctor.email = email
            doctor.mobile = mobile
            doctor.gender = gender
            doctor.address = address
            if profile_pic:
                doctor.profile_pic = profile_pic
            
            doctor.user.save()
            doctor.save()

            messages.success(request, 'Doctor details updated successfully')
            return redirect('viewDoctor')
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
    
    return render(request, 'admin/edit_doctor.html', {'doctor': doctor})




@login_required(login_url='login')
def viewDoctor(request):
    admin = get_object_or_404(Hoc, user=request.user)
    clinic = admin.clinic

    doctors = Doctor.objects.filter(status=True, clinic=clinic)
    return render(request, 'admin/view_doctor.html', {'doctors': doctors})



@login_required(login_url='/login/')
def admin_approve_doctor_view(request):
    # Those whose approval is needed
    doctors = Doctor.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_doctor.html', {'doctors': doctors})

@login_required(login_url='/login/')
def approve_doctor_view(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect('admin_approve_doctor')



@login_required(login_url='/login/')
def reject_doctor_view(request, pk):
    doctor = Doctor.objects.get(id=pk)
    user = User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin_approve_doctor')


@login_required(login_url='/login/')
def addPatient(request):
    clinics = Clinic.objects.all()
    doctors = Doctor.objects.filter(status=True)
    context = {
        'clinics': clinics,
        'doctors': doctors,
    }
    return render(request, 'admin/add_patient.html', context)




@login_required(login_url='/login/')
def savePatient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        email2 = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        id_no = request.POST.get('id_no')
        # clinic_id = request.POST.get('clinic')
        gender = request.POST.get('gender')
        home_distance = request.POST.get('home_distance')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type = '3',
            is_staff=False,
            is_superuser=False
        )

        admin = get_object_or_404(Hoc, user=request.user)
        clinic = admin.clinic

        patient = Patient(
            user=user,
            profile_pic=profile_pic,
            address=address,
            mobile=mobile,
            email=email2,
            id_no=id_no,
            clinic=clinic,
            gender=gender,
            home_distance=home_distance,
            status=True  # Assuming patients are approved by default
        )
        patient.save()
        messages.success(request, 'Patient added successfully!')
        return redirect('admin-patient-list')

    return redirect('addPatient')





@login_required(login_url='/login/')
def editPatient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    clinics = Clinic.objects.all()
    doctors = Doctor.objects.filter(status=True)
    context = {
        'patient': patient,
        'clinics': clinics,
        'doctors': doctors,
    }
    return render(request, 'admin/edit_patient.html', context)



@login_required(login_url='/login/')
def updatePatient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        user = patient.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        patient.address = request.POST.get('address')
        patient.mobile = request.POST.get('mobile')
        patient.id_no = request.POST.get('id_no')
        patient.clinic_id = request.POST.get('clinic')
        patient.gender = request.POST.get('gender')
        patient.home_distance = request.POST.get('home_distance')

        if 'profile_pic' in request.FILES:
            patient.profile_pic = request.FILES['profile_pic']
        
        patient.save()
        messages.success(request, 'Patient updated successfully!')
        return redirect('admin-patient-list')
    
    return redirect('editPatient', patient_id=patient_id)


@login_required(login_url='/login/')
def viewPatient(request):
    admin = get_object_or_404(Hoc, user=request.user)
    clinic = admin.clinic
    patients = Patient.objects.filter(clinic=clinic, status=True)

    return render(request, 'admin/view_patient.html', {'patients': patients})



@login_required(login_url='/login/')
def deletePatient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    # if request.method == 'POST':
    user = patient.user
    patient.delete()
    user.delete()
    messages.success(request, 'Patient deleted successfully!')
    return redirect('admin-patient-list')
    




@login_required(login_url='/login/')
def admin_approve_patient_view(request):
    # Filter patients needing approval
    patients = Patient.objects.filter(status=False)
    return render(request, 'admin/admin_approve_patient.html', {'patients': patients})



@login_required(login_url='/login/')
def approve_patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    messages.success(request, f'Patient {patient.get_name} approved successfully.')
    return redirect('admin-approve-patient')



@login_required(login_url='/login/')
def reject_patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    messages.success(request, f'Patient {patient.get_name} rejected and deleted successfully.')
    return redirect('admin-approve-patient')




@login_required(login_url='/login/')
def admin_discharge_patient_view(request):
    patients = Patient.objects.filter(status=True)
    return render(request, 'admin/admin_discharge_patient.html', {'patients': patients})


@login_required(login_url='/login/')
def discharge_patient_view(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    days = (date.today() - patient.admitDate).days
    assignedDoctor = User.objects.filter(id=patient.assignedDoctorId).first()
    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': days,
        'assignedDoctorName': assignedDoctor.first_name if assignedDoctor else '',
    }
    if request.method == 'POST':
        roomCharge = int(request.POST.get('roomCharge', 0))
        doctorFee = int(request.POST.get('doctorFee', 0))
        medicineCost = int(request.POST.get('medicineCost', 0))
        otherCharge = int(request.POST.get('otherCharge', 0))
        
        total = (roomCharge * days) + doctorFee + medicineCost + otherCharge
        
        pDD = PatientHospitalized.objects.create(
            patientId=pk,
            patientName=patient.get_name,
            assignedDoctorName=assignedDoctor.first_name if assignedDoctor else '',
            address=patient.address,
            mobile=patient.mobile,
            symptoms=patient.symptoms,
            admitDate=patient.admitDate,
            releaseDate=date.today(),
            daySpent=days,
            medicineCost=medicineCost,
            roomCharge=roomCharge * days,
            doctorFee=doctorFee,
            OtherCharge=otherCharge,
            total=total
        )
        
        context = {
            'patientName': patient.get_name,
            'assignedDoctorName': assignedDoctor.first_name if assignedDoctor else '',
            'address': patient.address,
            'mobile': patient.mobile,
            'symptoms': patient.symptoms,
            'admitDate': patient.admitDate,
            'releaseDate': date.today(),
            'daySpent': days,
            'medicineCost': medicineCost,
            'roomCharge': roomCharge * days,
            'doctorFee': doctorFee,
            'otherCharge': otherCharge,
            'total': total,
        }
        
        return render(request, 'admin/patient_final_bill.html', context)
    
    return render(request, 'admin/patient_generate_bill.html', patientDict)


@login_required(login_url='/login/')
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None





def download_pdf_view(request, pk):
    dischargeDetails = PatientHospitalized.objects.filter(patientId=pk).order_by('-id').first()
    
    if not dischargeDetails:
        return HttpResponse("No discharge details found for this patient.", status=404)
    
    context = {
        'patientName': dischargeDetails.patientName,
        'assignedDoctorName': dischargeDetails.assignedDoctorName,
        'address': dischargeDetails.address,
        'mobile': dischargeDetails.mobile,
        'symptoms': dischargeDetails.symptoms,
        'admitDate': dischargeDetails.admitDate,
        'releaseDate': dischargeDetails.releaseDate,
        'daySpent': dischargeDetails.daySpent,
        'medicineCost': dischargeDetails.medicineCost,
        'roomCharge': dischargeDetails.roomCharge,
        'doctorFee': dischargeDetails.doctorFee,
        'otherCharge': dischargeDetails.OtherCharge,
        'total': dischargeDetails.total,
    }
    
    pdf = render_to_pdf('admin/download_bill.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Patient_Bill_{dischargeDetails.patientName}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF.", status=500)




@login_required(login_url='/login/')
def admin_view_appointment(request):
    admin = get_object_or_404(Hoc, user=request.user)
    clinic = admin.clinic

    appointments = Appointment.objects.all().filter(status=True, clinic = clinic)
    context = {'appointments': appointments}
    return render(request, 'admin/admin_view_appointment.html', context)


from django.contrib.auth import get_user_model
User = get_user_model()
@login_required(login_url='/login/')
def admin_add_appointment_view(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        doctor_id = request.POST.get('doctorId')
        patient_id = request.POST.get('patientId')
        appointment_date = request.POST.get('appointmentDate')

        hoc = Hoc.objects.get(user=request.user)
        clinic = hoc.clinic
        
        if description and doctor_id and patient_id:

            doctor = Doctor.objects.get(user_id=doctor_id)
            patient = Patient.objects.get(user_id=patient_id)

            appointment = Appointment(
                description=description,
                doctorId=doctor,
                patientId=patient,
                doctorName=User.objects.get(id=doctor_id).first_name,
                patientName=User.objects.get(id=patient_id).first_name,
                clinic=clinic,
                appointmentDate=appointment_date,
                status=True
            )
            appointment.save()
            return HttpResponseRedirect(reverse('admin_view_appointment'))
        else:
            # Handle the case where form data is not valid
            pass

    admin = get_object_or_404(Hoc, user=request.user)
    clinic = admin.clinic

    doctors = Doctor.objects.all().filter(status=True, clinic=clinic)
    patients = Patient.objects.all().filter(status=True, clinic=clinic)
    context = {'doctors': doctors, 'patients': patients}
    return render(request, 'admin/admin_add_appointment.html', context)



@login_required(login_url='/login/')
def admin_approve_appointment_view(request):
    admin = get_object_or_404(Hoc, user=request.user)
    clinic = admin.clinic
    appointments = Appointment.objects.all().filter(status=False, clinic=clinic)
    return render(request, 'admin/admin_approve_appointment.html', {'appointments': appointments})


@login_required(login_url='/login/')
def approve_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin_approve_appointment'))


@login_required(login_url='/login/')
def reject_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.delete()
    return redirect(reverse('admin_approve_appointment'))



@login_required(login_url='/login/')
def admin_medecine_shop_view(request):
    query = request.GET.get('q')
    if query:
        medicines = Medicine.objects.filter(name__icontains=query) | Medicine.objects.filter(company__icontains=query)
    else:
        medicines = Medicine.objects.all()
    orders = OrderMedicine.objects.all().order_by('-order_date')
    return render(request, 'admin/admin_medecine_shop.html', {'medicines': medicines, 'query': query, 'orders': orders})




# def medicine_list(request):
#     medicines = Medicine.objects.all()
#     return render(request, 'admin/medicine_list.html', {'medicines': medicines})


@login_required(login_url='/login/')
def medicine_add(request):
    return render(request, 'admin/admin_medecine_shop_add.html', {'title': 'Add Medicine'})



@login_required(login_url='/login/')
def medicine_save(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            model = request.POST.get('model')
            type = request.POST.get('type')
            description = request.POST.get('description')
            company = request.POST.get('company')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            image = request.FILES.get('image')

            if not all([name, model, type, description, company, quantity, price]):
                raise ValueError("All fields are required.")
            
            quantity = int(quantity)
            price = float(price)

            Medicine.objects.create(
                name=name, 
                model=model, 
                type=type, 
                description=description, 
                company=company, 
                quantity=quantity, 
                price=price,
                image=image
            )
            messages.success(request, 'Medicine added successfully!')
            return redirect('admin_medecine_shop_view')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f'Error adding medicine: {e}')
    return redirect('medicine_add')



@login_required(login_url='/login/')
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        try:
            medicine.name = request.POST.get('name')
            medicine.model = request.POST.get('model')
            medicine.type = request.POST.get('type')
            medicine.description = request.POST.get('description')
            medicine.company = request.POST.get('company')
            medicine.quantity = request.POST.get('quantity')
            medicine.price = request.POST.get('price')
            image = request.FILES.get('image')

            if not all([medicine.name, medicine.model, medicine.type, medicine.description, medicine.company, medicine.quantity, medicine.price]):
                raise ValueError("All fields are required.")
            
            if image:
                medicine.image = image

            medicine.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('admin_medecine_shop_view')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f'Error updating medicine: {e}')
    return render(request, 'admin/admin_medicine_form_edit.html', {'medicine': medicine, 'title': 'Edit Medicine'})



@login_required(login_url='/login/')
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    try:
        medicine.delete()
        messages.success(request, 'Medicine deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting medicine: {e}')
    return redirect('admin_medecine_shop_view')






@login_required(login_url='/login/')
def view_orders_view(request):
    orders = OrderMedicine.objects.all()
    return render(request, 'admin/view_medicine_orders.html', {'orders': orders})






@login_required(login_url='/login/')
def admin_test_view(request):
    query = request.GET.get('q')
    if query:
        tests = Test.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        tests = Test.objects.all()

    orders = OrderTest.objects.all().order_by('-order_date')
    return render(request, 'admin/admin_test_view.html', {'tests': tests, 'query': query, 'orders': orders})


@login_required(login_url='/login/')
def test_add(request):
    return render(request, 'admin/admin_test_add.html', {'title': 'Add Test'})


@login_required(login_url='/login/')
def test_save(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')

            if not all([name, description, price]):
                raise ValueError("All fields are required.")
            
            price = float(price)

            Test.objects.create(
                name=name, 
                description=description, 
                price=price
            )
            messages.success(request, 'Test added successfully!')
            return redirect('admin_test_view')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f'Error adding test: {e}')
    return redirect('test_add')


@login_required(login_url='/login/')
def test_edit(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        try:
            test.name = request.POST.get('name')
            test.description = request.POST.get('description')
            test.price = request.POST.get('price')

            if not all([test.name, test.description, test.price]):
                raise ValueError("All fields are required.")
            
            test.price = float(test.price)
            test.save()
            messages.success(request, 'Test updated successfully!')
            return redirect('admin_test_view')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f'Error updating test: {e}')
    return render(request, 'admin/admin_test_form_edit.html', {'test': test, 'title': 'Edit Test'})


@login_required(login_url='/login/')
def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    try:
        test.delete()
        messages.success(request, 'Test deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting test: {e}')
    return redirect('admin_test_view')



def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def is_admin(user):
    return user.is_staff





@login_required(login_url='login')
def create_test_report_view(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    tests = Test.objects.all()
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        result = request.POST.get('result')
        doctor = request.user if is_doctor(request.user) else None

        test = get_object_or_404(Test, id=test_id)
        TestReport.objects.create(patient=patient, doctor=doctor, test=test, result=result)

        messages.success(request, 'Test report submitted successfully.')
        return redirect('view_patient_reports', patient_id=patient.id)

    return render(request, 'admin/create_test_report.html', {'patient': patient, 'tests': tests})




@login_required(login_url='login')
def appointed_patients_view(request):
    # if request.user.groups.filter(name='HOC').exists():
    admin = Hoc.objects.get(user=request.user)
    doctors = Doctor.objects.filter(clinic=admin.clinic)
    # else:
    #     doctors = Doctor.objects.none()  # Or handle as appropriate
    
    patients = Patient.objects.filter(clinic = admin.clinic)
    appointed_patients = Appointment.objects.filter(status=True)
    tests = Test.objects.all()
    return render(request, 'admin/submit_test_report.html', {
        'patients': patients,
        'tests': tests,
        'appointed_patients': appointed_patients,
        'doctors': doctors
    })





@login_required(login_url='login')
def submit_test_report(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        test_ids = request.POST.getlist('test_ids')
        result = request.POST.get('result')

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)  # Correctly get doctor based on CustomUser ID

        tests = Test.objects.filter(id__in=test_ids)

        test_report = TestReport.objects.create(patient=patient, doctor=doctor, result=result)
        test_report.test.set(tests)
        test_report.save()

        messages.success(request, 'Test report submitted successfully.')
    return redirect('appointed_patients')

    # return JsonResponse({'error': 'Invalid request'}, status=400)