from django import forms
from attendance.models import*

class UploadEmpForm(forms.Form):
    excelFile = forms.FileField(label='Select an excel file')

    def cleanExcel(self):
        file = self.cleaned_data.get('excelFile')
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('Invalid file type. Please upload an Excel file with .xlsx extension.')
        return file
    
class AddEmpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields =  ['IFID','EmpName','Mobile']
        widgets = {
            'IFID':forms.TextInput(attrs={'placeholder':'IFID'}),
            'EmpName':forms.TextInput(attrs={'placeholder':'NAME'}),
            'Mobile':forms.TextInput(attrs={'placeholder':'MOB'})
        }       

# class MonthYearForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['month','year']
#         widgets = {
#             'month':forms.Select(choices=Attendance.MONTH_CHOICES),
#             'year':forms.NumberInput(attrs={'placeholder':'YYYY'})
#         }

# class UploadAttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['attendanceSheet']