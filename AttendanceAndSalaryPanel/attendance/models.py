from django.db import models


# Create your models here.

class Employee(models.Model):
    IFID = models.CharField(max_length=20,unique=True)
    EmpName = models.CharField(max_length=150,db_index=True)
    Mobile = models.CharField(max_length=10)
    excelFile = models.FileField(upload_to='EmployeeList/',blank=True,null=True)

    def __str__(self):
        return f"f'{self.IFID} - {self.EmpName}'"
    
class AttendanceMonth(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]

    Month = models.CharField(max_length=20,choices=MONTH_CHOICES)
    Year = models.IntegerField()

    class Meta:
        unique_together = ('Month', 'Year')  # Ensure unique month-year pair

    def __str__(self):
        return f"{dict(self.MONTH_CHOICES)[self.Month]} ({self.Year})"


class AttendanceSheet(models.Model):
    Month = models.ForeignKey(AttendanceMonth, on_delete=models.CASCADE, related_name="attendance_sheets")
    AttendanceFile = models.FileField(upload_to='attendance_sheets/')

    def __str__(self):
        return f"Attendance sheet for {self.Month}"
    
class Attendance(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    User = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    Month = models.ForeignKey(AttendanceMonth, on_delete=models.CASCADE, related_name="attendances")
    AttendanceSheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name="attendances")
    WFH = models.IntegerField(default=0)
    WFO = models.IntegerField(default=0)
    OT = models.IntegerField(default=0)
    Punchingmistake = models.IntegerField(default=0)
    Deduction = models.IntegerField(default=0)
    NightShift = models.IntegerField(default=0)
    Total = models.IntegerField(default=0)
    PunchingFile = models.FileField(upload_to='punching_files/')

    def __str__(self):
        return f"{self.Employee.EmpName} Attendance for {self.Month}"
    


    