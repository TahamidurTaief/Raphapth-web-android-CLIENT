
from django.contrib import admin
from django.urls import path, include
from . import views , HOC_views, DOCTOR_views, PATIENT_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.website, name='website'),
    path('contact/', views.contact_view, name='contact'),


    path('superadmin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('dologin/', views.DoLogin, name='dologin'),
    path('doLogout/', views.doLogout, name='logout'),
    path('signup/doctor/', views.signupDoctor, name='signupDoctor'),
    path('signup/patient/', views.signupPatient, name='signupPatient'),
    # path('signup/', views.signup_view, name='signup'),
    
    path('signup/', views.signup_view, name='signup'),
    



    path('admin-dashboard/', HOC_views.AdminDashboard, name='AdminDashboard'),
    path('admin/doctor/add', HOC_views.addDoctor, name='addDoctor'),
    path('admin/doctor/save', HOC_views.saveDoctor, name='saveDoctor'),
    path('admin/doctor/', HOC_views.viewDoctor, name='viewDoctor'),
    path('admin/doctor/delete/<int:doctor_id>/', HOC_views.deleteDoctor, name='deleteDoctor'),

    path('admin/approve-doctor/', HOC_views.admin_approve_doctor_view, name='admin_approve_doctor'),
    path('admin/approve-doctor/<int:pk>/', HOC_views.approve_doctor_view, name='approve_doctor'),
    path('admin/reject-doctor/<int:pk>/', HOC_views.reject_doctor_view, name='reject_doctor'),
    path('doctor/edit/<int:doctor_id>/', HOC_views.editDoctor, name='doctor_edit'),
    path('admin/patient/add/', HOC_views.addPatient, name='admin-add-patient'),
    path('admin/patient/save/', HOC_views.savePatient, name='admin-save-patient'),
    path('admin/patient/list/', HOC_views.viewPatient, name='admin-patient-list'),
    path('admin/approve/patient/', HOC_views.admin_approve_patient_view, name='admin-approve-patient'),
    path('admin/approve/patient/<int:pk>/', HOC_views.approve_patient_view, name='admin-approve-patient'),
    path('admin/reject/patient/<int:pk>/', HOC_views.reject_patient_view, name='admin-reject-patient'),


    path('admin/discharge-patients/', HOC_views.admin_discharge_patient_view, name='admin_discharge_patients'),
    path('discharge-patient/<int:pk>/', HOC_views.discharge_patient_view, name='discharge_patient'),
    path('download-pdf/<int:pk>/', HOC_views.download_pdf_view, name='download_pdf'),
    path('patient/<int:patient_id>/edit', HOC_views.editPatient, name='admin-edit-patient'),
    path('patient/<int:patient_id>/update', HOC_views.updatePatient, name='admin-update-patient'),
    path('patient/<int:patient_id>/delete', HOC_views.deletePatient, name='admin-delete-patient'),


    path('admin-add-appointment/', HOC_views.admin_add_appointment_view, name='admin_add_appointment_view'),
    path('admin-view-appointment/', HOC_views.admin_view_appointment, name='admin_view_appointment'),
    path('admin-approve-appointment/', HOC_views.admin_approve_appointment_view, name='admin_approve_appointment'),
    path('approve-appointment/<int:pk>/', HOC_views.approve_appointment_view, name='approve_appointment'),
    path('reject-appointment/<int:pk>/', HOC_views.reject_appointment_view, name='reject_appointment'),


    path('admin/medecine/shop/', HOC_views.admin_medecine_shop_view, name='admin_medecine_shop_view'),
    # path('admin/medicine/list/', views.medicine_list, name='medicine_list'),
    path('admin/medicine/add/', HOC_views.medicine_add, name='medicine_add'),
    path('admin/medicine/save/', HOC_views.medicine_save, name='medicine_save'),
    path('admin/medicine/edit/<int:pk>/', HOC_views.medicine_edit, name='medicine_edit'),
    path('admin/medicine/delete/<int:pk>/', HOC_views.medicine_delete, name='medicine_delete'),
    path('admin/medicine/orders/view', HOC_views.view_orders_view, name='view_medicine_orders'),

    path('admin/test/view/', HOC_views.admin_test_view, name='admin_test_view'),
    path('admin/test/add/', HOC_views.test_add, name='test_add'),
    path('admin/test/save/', HOC_views.test_save, name='test_save'),
    path('admin/test/edit/<int:pk>/', HOC_views.test_edit, name='test_edit'),
    path('admin/test/delete/<int:pk>/', HOC_views.test_delete, name='test_delete'),

    path('admin/appointed/patients/', HOC_views.appointed_patients_view, name='appointed_patients'),
    path('admin/submit/test/report/', HOC_views.submit_test_report, name='submit_test_report'),











    path('doctor/dashboard/', DOCTOR_views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/view/appointment/', DOCTOR_views.doctor_view_appointment_view, name='doctor_view_appointment'),
    path('doctor/view/appointment/', DOCTOR_views.doctor_view_appointment_view, name='doctor_view_appointment'),
    path('doctor/delete/appointment/', DOCTOR_views.doctor_delete_appointment_view, name='doctor_delete_appointment_view'),
    path('delete/appointment/<int:pk>/', DOCTOR_views.delete_appointment_view, name='delete-appointment'),




    path('patient/dashboard/', PATIENT_views.patientDashboard, name='patient_dashboard'),
    path('patient/appointments/', PATIENT_views.patient_appointment_view, name='patient_appointment_view'),
    path('patient/book/appointment/', PATIENT_views.patient_book_appointment_view, name='patient_book_appointment_view'),

    path('patient-view-doctor/', PATIENT_views.patient_view_doctor_view, name='patient_view_doctor_view'),
    path('searchdoctor/', PATIENT_views.search_doctor_view, name='search_doctor_view'),

    path('medicine-shop/', PATIENT_views.medicine_shop_view, name='medicine_shop'),
    path('purchase-medicine/<int:pk>/', PATIENT_views.purchase_medicine_view, name='purchase_medicine'),
    path('process-order/<int:pk>/', PATIENT_views.process_order_view, name='process_order'),

    path('patient/test/view', PATIENT_views.test_view, name='test_view'),
    path('patient/test/reports/', PATIENT_views.patient_test_reports_view, name='patient_test_reports'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
