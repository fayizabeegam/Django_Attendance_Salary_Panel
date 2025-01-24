from django.db import models
from attendance.models import Employee
# Create your models here.



class SalaryMonth(models.Model):
    Month = models.CharField(max_length=20)
    Year = models.IntegerField()

    def __str__(self):
        return f"{self.Month} {self.Year}"
    

class SalarySheet(models.Model):
    Month = models.ForeignKey(SalaryMonth, on_delete=models.CASCADE)
    SalaryFile = models.FileField(upload_to='salary_sheets/')

    def __str__(self):
        return f"Salary Sheet for {self.Month}"


class Salary(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    BasicSalary = models.DecimalField(max_digits=10, decimal_places=2)
    SpecialIncome = models.DecimalField(max_digits=10, decimal_places=2)
    Deduction = models.DecimalField(max_digits=10, decimal_places=2)
    GrandTotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Salary for {self.Employee.EmpName} - Total: {self.GrandTotal}"
    

