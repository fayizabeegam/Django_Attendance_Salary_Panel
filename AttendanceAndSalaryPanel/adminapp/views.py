from accounts.models import*
from .forms import*
import pandas as pd
from django.db.models import Q
from attendance.models import*
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# Create your views here.

"""
    Admin dashboard
"""

@method_decorator(login_required,name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'Admin/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_navbar'] = True 
        return context

@method_decorator(login_required, name='dispatch')
class UploadBulkEmpView(View):
    form_class = UploadEmpForm
    template_name = 'Admin/accounts.html'

    def get(self, request):
        form = self.form_class()
        employees = Employee.objects.all()
        return render(request, self.template_name, {'form': form, 'employees': employees, 'show_navbar': True})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        employees = Employee.objects.all()
        
        if form.is_valid():
            excelFile = request.FILES.get('excelFile')
            if excelFile:
                try:
                    # Validate file extension
                    file_ext = excelFile.name.split('.')[-1].lower()
                    if file_ext == 'xls':
                        xl = pd.ExcelFile(excelFile, engine='xlrd')
                    elif file_ext == 'xlsx':
                        xl = pd.ExcelFile(excelFile, engine='openpyxl')
                    else:
                        return render(request, self.template_name, {
                            'form': form,
                            'employees': employees,
                            'error': "Unsupported file format. Please upload .xls or .xlsx files.",
                        })

                    # Process the Excel file
                    for name in xl.sheet_names:
                        df = xl.parse(sheet_name=name)
                        if {'IFID', 'NAME', 'Mobile number'}.issubset(df.columns):
                            for _, row in df.iterrows():
                                ifid = row['IFID'] if pd.notna(row['IFID']) else None
                                emp_name = row['NAME'] if pd.notna(row['NAME']) else None
                                mobile_number = row['Mobile number'] if pd.notna(row['Mobile number']) else None
                                 # Validate mobile number length
                                if mobile_number and len(str(mobile_number)) != 10:
                                    messages.error(request, f"Invalid mobile number for {emp_name}. Must be 10 digits.")
                                    continue

                                Employee.objects.update_or_create(
                                    IFID=ifid,
                                    defaults={
                                        'EmpName': emp_name,
                                        'Mobile': mobile_number
                                    }
                                )

                    # Refresh employees after updating
                    employees = Employee.objects.all()
                    success_message = "Employee data uploaded successfully!"
                    return render(request, self.template_name, {
                        'form': self.form_class(),
                        'employees': employees,
                        'show_navbar': True,
                        'success': success_message,
                    })
                except Exception as e:
                    return render(request, self.template_name, {
                        'form': form,
                        'employees': employees,
                        'show_navbar': True,
                        'error': f"Error processing the file: {str(e)}",
                    })

        # If the form is invalid, re-render with errors
        return render(request, self.template_name, {'form': form, 'employees': employees,'show_navbar': True})




@method_decorator(login_required,name='dispatch')
class EmployeeListView(ListView):
    model = Employee
    template_name = 'Admin/accounts.html'
    context_object_name = 'employees'

    def get(self, request):
        # Fetch employees and prepare the form
        employees = Employee.objects.all()
        form = AddEmpForm()
        return render(request, self.template_name, {
            'employees': employees,
            'form': form,
            'show_navbar': True
        })

    def post(self, request):
        # Handle form submission for adding a new employee
        form = AddEmpForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('Mobile')
            form.save()
            messages.success(request, "Employee added successfully.")
        else:
            messages.error(request, "Error adding employee.")
        
        # Redirect to the same view to reload the full template
        return redirect('adminapp:employee-list')


@method_decorator(login_required,name='dispatch')
class AddEmpView(CreateView):
    model = Employee
    form_class = AddEmpForm
    template_name = 'Admin/accounts.html'
    success_url = reverse_lazy('adminapp:employee-list')

    def form_valid(self,form):
        messages.success(self.request,'Employee added successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Error adding employee')
        return super().form_invalid(form)




@method_decorator(login_required,name='dispatch')
class EditEmpView(UpdateView):
    model = Employee
    form_class = AddEmpForm
    template_name = 'Admin/accounts.html'
    success_url = reverse_lazy('adminapp:employee-list')

    def form_valid(self, form):
        messages.success(self.request,'Edited successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Employee added successfully')
        return super().form_invalid(form)
             
             
@method_decorator(login_required,name='dispatch')                                                                                                   
class DeleteEmpView(DeleteView):
    model = Employee
    template_name = 'Admin/accounts.html'
    success_url = reverse_lazy('adminapp:employee-list')

    def get_object(self, queryset=None):
        """Ensure the object is found or return 404."""
        return get_object_or_404(Employee, pk=self.kwargs['pk'])
                                                   
    def delete(self,request,*args,**kwargs):
        messages.success(self.request,'Deleted successfully')
        return super().delete(request,*args,**kwargs)


       
@method_decorator(login_required,name='dispatch') 
class SearchEmployeeView(ListView):
    model = Employee
    template_name = 'Admin/accounts.html'
    context_object_name  = 'employees'

    def get_queryset(self):
        query = self.request.GET.get('search_query', '').strip()  # Get the search query from the URL
        
        if query:
            # Search for employees matching the IFID or name (case insensitive)
            employees = Employee.objects.filter(
                Q(IFID__iexact=query) |  # Exact match for IFID
                Q(EmpName__icontains=query)  # Partial match for Employee Name
            )
            print(f"Filtered Employees: {employees}")
            return employees
        
        # If no query, return all employees
        return Employee.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_navbar'] = True  # Add any other context variables needed
        context['search_query'] = self.request.GET.get('search_query', '')  # Pass search_query to template
        return context


