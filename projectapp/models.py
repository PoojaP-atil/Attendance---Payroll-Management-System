from django.db import models

# Create your models here.
class employee(models.Model):
    gender = (('Male','Male'),('Female','Female')) 
    Photo = models.ImageField(upload_to='media')
    Name = models.CharField(max_length=200)
    Gender = models.CharField(max_length=200, choices = gender)
    DOB = models.DateField()
    Designation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    Head = models.CharField(max_length=200,default='')
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNo = models.BigIntegerField()  
    Email = models.EmailField()
    Password = models.CharField(max_length=200)
    Salary = models.FloatField(default=0)
    slug = models.SlugField(default='',null=False)

    class Meta:
        db_table = 'employee'

class hr(models.Model):
    Name = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    Email = models.EmailField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = 'hr'

class accountant(models.Model):
    Name = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    Email = models.EmailField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = 'accountant'

class head(models.Model):
    gender = (('Male','Male'),('Female','Female')) 
    Photo = models.ImageField(upload_to='media')
    Name = models.CharField(max_length=200)
    Gender = models.CharField(max_length=200, choices = gender)
    DOB = models.DateField()
    Designation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNo = models.BigIntegerField()  
    Email = models.EmailField()
    Password = models.CharField(max_length=200)
    Salary = models.FloatField(default=0)
    slug = models.SlugField(default='',null=False)

    class Meta:
        db_table = 'head'

class attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    date = models.DateField(max_length=200,default='')
    status = models.CharField(max_length=100,default='')
    in_time = models.CharField(max_length=200,default='')
    out_time = models.CharField(max_length=200,default='')

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} on {self.date}"
    
class account(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    present = models.IntegerField()
    absent = models.IntegerField()
    totalworkingdays = models.IntegerField()
    paymenttobepaid = models.FloatField()

    class Meta:
        db_table = 'account'

class LeaveRequest(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2)
    reason = models.CharField(max_length=500)
    datefrom = models.DateField(max_length=200)
    datetill = models.DateField(max_length=200)
    is_approved = models.CharField(max_length=200,default='Unapproved')

