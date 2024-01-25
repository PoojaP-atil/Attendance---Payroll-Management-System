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
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNo = models.BigIntegerField()  
    Email = models.EmailField()
    Password = models.CharField(max_length=200)
    slug = models.SlugField(default='',null=False)

    class Meta:
        db_table = 'employee'

class admins(models.Model):
    Name = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    Email = models.EmailField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = 'admins'

class attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    date = models.DateField(max_length=200,default='')
    status = models.CharField(max_length=100,default='')
    in_time = models.CharField(max_length=200,default='')
    out_time = models.CharField(max_length=200,default='')