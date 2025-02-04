from django.urls import path,re_path
from .views import*
from django.conf import settings
from django.conf.urls.static import static


app_name = "adminapp"

urlpatterns = [
    path('admin_dashboard/',AdminDashboardView.as_view(),name='admin-dashboard'),
    path('accounts_menu/',AccountsMenuView.as_view(),name='accounts-menu'),
    path('employee_list/',EmployeeListView.as_view(),name='employee-list'),
    path('upload_employees/', UploadBulkEmpView.as_view(), name = 'upload-employee-details'),
    path('add_employees/',AddEmpView.as_view(), name = 'add-employees'),
    path('employee/edit/<int:pk>/', EditEmpView.as_view(), name='edit-employee'),  
    path('employees/delete/<int:pk>/', DeleteEmpView.as_view(), name='delete-employee'), 
    path('search_employees/', SearchEmployeeView.as_view(), name='search-employee')
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
