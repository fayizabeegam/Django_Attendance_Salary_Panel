from django.db import models
from attendance.models import Employee
# Create your models here.

class HrConversion(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Employee.EmpName} {self.Department}"