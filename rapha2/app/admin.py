from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'user_type']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'email', 'clinic', 'status', 'created_at', 'updated_at']
    
    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    get_name.short_description = 'Name'


class HocAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'phone', 'clinic', 'created_at', 'updated_at']
    
    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    get_name.short_description = 'Name'


class PatientAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'email', 'mobile', 'clinic', 'admitDate', 'status', 'created_at', 'updated_at']
    
    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    get_name.short_description = 'Name'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patientName', 'doctorName', 'appointmentDate', 'description', 'status', 'clinic', 'created_at']


class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'type', 'company', 'quantity', 'price', 'is_in_stock']


class OrderMedicineAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'medicine', 'order_date', 'order_quantity', 'payment_method', 'transaction_id']


class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']


class OrderTestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'test', 'order_date', 'payment_method', 'transaction_id']


class TestReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date']


class WebAboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)


class WebContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'message')


class LatestArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialist', 'created_at')


class WebSpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')




admin.site.register(Web_Specialist, WebSpecialistAdmin)
admin.site.register(Web_About_us, WebAboutUsAdmin)
admin.site.register(Web_Contact_us, WebContactUsAdmin)
admin.site.register(Web_Latest_Articles, LatestArticlesAdmin)

admin.site.register(Hoc, HocAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Clinic)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(OrderMedicine, OrderMedicineAdmin)
admin.site.register(TestReport, TestReportAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(OrderTest, OrderTestAdmin)
admin.site.register(Medicine, MedicineAdmin)
