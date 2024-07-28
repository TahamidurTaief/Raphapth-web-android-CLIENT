from telnetlib import LOGOUT
from django.shortcuts import redirect, render, HttpResponse
# from app.EmailBackEnd import EmailBackend
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import *
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage





def website(request):
    articles = Web_Latest_Articles.objects.all().order_by('-id')[:3]
    latest_about_us = Web_About_us.objects.all().order_by('-id')[:1]
    specialists = Web_Specialist.objects.all().order_by('-id')[:6]

    context = {
        'articles': articles,
        'about_us': latest_about_us,
        'specialists': specialists,
    }
    return render(request, 'web.html', context)



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('text')


        if name and phone and message:
            Web_Contact_us.objects.create(
                name=name,
                phone=phone,
                message=message
            )
            return redirect('website')
        else:
            messages.error(request, 'Please fill all the fields')
            return redirect('website')

    return render(request, 'contact.html')





def signup_view(request):
    clinics = Clinic.objects.all()

    context = {
        'clinics': clinics
    }

    return render(request, 'signup.html', context)


def login(request):
    return render(request, 'login.html')


def DoLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.user_type == '1':
                return redirect('AdminDashboard')
            elif user.user_type == '2':
                return redirect('doctor_dashboard')
            elif user.user_type == '3':
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid user type')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    # else:
    #     return render(request, 'login.html')
    


from django.contrib.auth import logout
def doLogout(request):
    logout(request)
    return redirect('login')






def signupDoctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        clinic_id = request.POST.get('clinic')
        address = request.POST['address']
        profile_pic = request.FILES.get('profile_pic')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            try:
                clinic = Clinic.objects.get(id=clinic_id)
                user = CustomUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_staff=False,
                    is_superuser=False
                )
                user.user_type = 2
                user.save()
                
                doctor = Doctor(
                    user=user,
                    gender=gender,
                    mobile=mobile,
                    address=address,
                    clinic=clinic
                )
                if profile_pic:
                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    doctor.profile_pic = fs.url(filename)
                
                doctor.save()
                messages.success(request, 'Doctor registered successfully. You can login when admin will approve your account.')
                return redirect('doctor_dashboard')
            except Exception as e:
                messages.error(request, 'Error: ' + str(e))
    clinics = Clinic.objects.all()
    return render(request, 'signup.html', {'clinics': clinics})




def signupPatient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        id_no = request.POST.get('id_no')
        clinic_id = request.POST.get('clinic')
        gender = request.POST.get('gender')
        home_distance = request.POST.get('home_distance')

        try:
            clinic = Clinic.objects.get(id=clinic_id)
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,
                is_superuser=False
            )
            user.user_type = 3
            user.save()

            patient = Patient(
                user=user,
                profile_pic=profile_pic,
                address=address,
                mobile=mobile,
                email=email,
                id_no=id_no,
                clinic=clinic,
                gender=gender,
                home_distance=home_distance,
                status=True
            )
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                patient.profile_pic = fs.url(filename)

            patient.save()
            messages.success(request, 'Patient added successfully!')
            return redirect('admin-patient-list')
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))

    clinics = Clinic.objects.all()
    return render(request, 'signup.html', {'clinics': clinics})



# def sidebar(request):
#     user = request.user
#     user_name = user.first_name + ' ' + user.last_name
#     user_type = user.user_type
#     user_pic = user.profile_pic.url

#     print(f"\n\n{user_name}\n{user_type}\n{user_pic}\n\n")
#     return render(request, 'sidebar.html')