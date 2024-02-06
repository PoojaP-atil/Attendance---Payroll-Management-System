from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse, HttpResponseBadRequest
from projectapp.models import employee, hr,attendance, head,account,Event,accountant,LeaveRequest,payment
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.urls import reverse
import calendar
from django.core.mail import EmailMessage
import holidays

# Create your views here.
def EmpListView(request):
    if 'hr' in request.session:
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
        employ = employee.objects.all()
        print(hrs)
        return render(request,'home.html',{'hr':empobj,'employ':employ})
    
    elif 'head' in request.session:
        head1 = request.session['head']
        empobj = head.objects.get(Email = head1)
        employ = employee.objects.filter(Head = empobj.Name)
        print(head1)
        return render(request,'home.html',{'head':empobj,'employ':employ})
    
    elif 'acc' in request.session:
        acc = request.session['acc']
        empobj = accountant.objects.get(Email = acc)
        employ = employee.objects.all()
        print(acc)
        return render(request,'acchome.html',{'head':empobj,'employ':employ})

def EmpDetailView(request,slug):
    if 'hr' in request.session:
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
        employ = employee.objects.get(slug = slug)
        return render(request,'empdetail.html',{'hr':empobj,'empdetail':employ})
    
    elif 'head' in request.session:
        head1 = request.session['head']
        empobj = head.objects.get(Email = head1)
        employ = employee.objects.get(slug = slug)
        return render(request,'empdetail.html',{'head':empobj,'empdetail':employ})

def accempview(request,slug):    
    if 'acc' in request.session:
        acc = request.session['acc']
        empobj = accountant.objects.get(Email = acc)
        employ = employee.objects.get(slug = slug)
        attobj = attendance.objects.filter(employee=empobj.id)
        return render(request,'accempdetail.html',{'head':empobj,'empdetail':employ,'attobj':attobj})

def Editemp(request,slug):
    if request.method =='GET':
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
        employ = employee.objects.get(slug = slug)
        return render(request,'editform.html',{'user':empobj,'empdetail':employ})
    elif request.method =='POST':
        hrs = request.session['hr']
        empobj = hr.objects.get(Email = hrs)
        employ = employee.objects.get(slug = slug)
        employ.Name = request.POST.get('fname')
        employ.Address = request.POST.get('address')
        employ.City = request.POST.get('city')
        employ.State = request.POST.get('state')
        employ.Pincode = request.POST.get('pincode')
        employ.PhoneNo = request.POST.get('phone')
        employ.Email = request.POST.get('email')
        employ.Photo = request.FILES.get('photo')
        employ.save()
        return render(request,'empdetail.html',{'user':empobj,'empdetail':employ})

#navbar for hrpage
def hrmain(request):
    return render(request,'hrmain.html')

#after hr login
def hrhome(request):
    if 'hr' in request.session:
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
        return render(request, 'hrindex.html', {'hr': hrobj,'empdetail': hrobj})
    
    
    
#delete user profile from hr
def deleteprofile(request,slug):
    if 'hr' in request.session:
        hrs= request.session.get('hr')
        hrobj= hr.objects.get(Email=hrs)
        obj = employee.objects.get(slug=slug)
        obj.delete()
        return redirect('../../hrhome/')
    
#hr edit user details   
def editemphr(request,slug):
    if 'hr' in request.session:
        if request.method =='GET':
            hrs= request.session['hr']
            hrobj= hr.objects.get(Email=hrs)
            employ = employee.objects.get(slug = slug)
            return render(request,'editformhrend.html',{'hr':hrobj,'empdetail':employ})
        elif request.method =='POST':
            hrs= request.session['hr']
            hrobj= hr.objects.get(Email=hrs)
            employ = employee.objects.get(slug = slug)
            employ.Name = request.POST.get('fname')
            employ.Address = request.POST.get('address')
            employ.City = request.POST.get('city')
            employ.State = request.POST.get('state')
            employ.Pincode = request.POST.get('pincode')
            employ.PhoneNo = request.POST.get('phone')
            employ.Email = request.POST.get('email')
            employ.Photo = request.FILES.get('photo')
            employ.Designation = request.POST.get('designation')
            employ.Department = request.POST.get('department')
            employ.Head = request.POST.get('sectionhead')
            employ.save()
            return render(request,'empdetail.html',{'hr':hrobj,'empdetail':employ})
        
    elif 'head' in request.session:
        if request.method =='GET':
            head1= request.session['head']
            hrobj= head.objects.get(Email=head1)
            employ = employee.objects.get(slug = slug)
            return render(request,'editformhrend.html',{'head':hrobj,'empdetail':employ})
        elif request.method =='POST':
            head1= request.session['head']
            hrobj= head.objects.get(Email=head1)
            employ = employee.objects.get(slug = slug)
            employ.Name = request.POST.get('fname')
            employ.Address = request.POST.get('address')
            employ.City = request.POST.get('city')
            employ.State = request.POST.get('state')
            employ.Pincode = request.POST.get('pincode')
            employ.PhoneNo = request.POST.get('phone')
            employ.Email = request.POST.get('email')
            employ.Photo = request.FILES.get('photo')
            employ.save()
            return render(request,'empdetail.html',{'head':hrobj,'empdetail':employ})
    
#update user attendance from hr end
# def update(request,id):
#     if request.method == 'GET':
#         if 'hr' in request.session:
#             hrs= request.session.get('hr')
#             hrobj= hr.objects.get(Email=hrs)
#             obj = attendance.objects.get(id=id)
#             return render(request,'showattendance.html',{'hr':hrobj,'obj':obj})
#     elif request.method =='POST':
#         if 'hr' in request.session:
#             hr= request.session.get('hr')
#             hrobj= hr.objects.get(Email=hr)
#             dates = request.POST['date']
#             print(dates)
#             intime = request.POST.get('in_time')
#             outtime = request.POST.get('out_time')
#             statuss = request.POST.get('status')
#             upobj = attendance.objects.get(id=id)
#             upobj.date = dates
#             upobj.in_time = intime
#             upobj.out_time = outtime
#             upobj.status = statuss
#             upobj.save()
#             return redirect('../../showattendance/')

def searchbox(request):
    if request.method == "POST":
        sq= request.POST.get('search_query')
        result = employee.objects.filter(Q(Name__icontains= sq) | Q(Designation__icontains= sq) | Q(Department__icontains= sq)|Q(Gender__iexact= sq))
        return render(request, 'home.html', {'listobj':result})

#hr login
def hrlogin(request):
    if request.method=="GET":
        return render(request,"hrlogin.html")
    elif request.method=="POST":
        hrs = request.POST['email']
        hrobj = hr.objects.filter(Email = hrs)
        if hrobj:
            hrobj = hr.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,hrobj.Password)

            if flag:
                request.session['hr'] = request.POST.get('email')
                return redirect("../hrheadhome/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'hrlogin.html',{'msg':error_message})

        elif head.objects.get(Email = hrs):
            headobj = head.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,headobj.Password)

            if flag:
                request.session['head'] = request.POST.get('email')
                return redirect("../hrheadhome/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'hrlogin.html',{'msg':error_message})
        else:
            error_message = "No User found"
            return render(request,'hrlogin.html',{'msg':error_message})

#accountant login
def acclogin(request):
    if request.method=="GET":
        return render(request,"acclogin.html")
    elif request.method=="POST":
        acc = request.POST['email']
        accobj = accountant.objects.filter(Email = acc)
        if accobj:
            accobj = accountant.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,accobj.Password)

            if flag:
                request.session['acc'] = request.POST.get('email')
                return redirect("../hrheadhome/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'acclogin.html',{'msg':error_message})
            
        else:
            error_message = "No User found"
            return render(request,'acclogin.html',{'msg':error_message})

#hr logout       
def hrlogout(request):
    request.session['email'] = ''
    return redirect('../hr-login/')  

#hrregister
def hrregister(request):
    if request.method=="GET":
        return render(request,"hrregister.html")
    elif request.method=="POST":
        name = request.POST.get("fname")
        designation = request.POST.get("designation")
        department = request.POST.get("department")
        email =request.POST.get("email")
        password= request.POST.get("password")
        passw = make_password(password)
        hrobj = hr(Name=name, Designation=designation,Department=department,Email=email,Password=passw)
        hrobj.save()

        return HttpResponse("hr registered Successfully")

#user view

#user login
def userlogin(request):
    if request.method=="GET":
        return render(request,"userlogin.html")
    elif request.method=="POST":
        emp = employee.objects.filter(Email = request.POST.get("email"))

        if emp:
            empobj = employee.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("password")
            flag = check_password(passfe,empobj.Password)

            if flag:
                request.session['user'] = request.POST.get('email')
                return redirect("../index/")
            else:
                error_message = "Wrong credentials !! Oops try again :("
                return render(request,'userlogin.html',{'msg':error_message})

        else:
                error_message = "No user found"
                return render(request,'userlogin.html',{'msg':error_message})

#user logout      
def userlogout(request):
    request.session['user'] = ''
    return redirect('../user-login/')  

#user regiseter
def userregister(request):
    if request.method=="GET":
        return render(request,"userregister.html")
    elif request.method=="POST":
        if request.POST.get('designation') == 'Section Head':
            name = request.POST.get("fname")
            photo =request.FILES.get("photo")
            gender = request.POST.get("gender")
            dateofbirth = request.POST.get("DOB")
            address = request.POST.get("address")
            state = request.POST.get("state")
            city = request.POST.get("city")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            pincode = request.POST.get("pincode")
            phoneno = request.POST.get("phone")
            email =request.POST.get("email")
            password= request.POST.get("password")
            salary = request.POST.get('salary')
            passw = make_password(password)
            slugobj = name+'-'+designation
            head1 = 'HR'
            empobj = head(Name=name, Salary=salary, Photo = photo,Gender=gender,Designation=designation,Department=department, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
            empobj.save()
            emp1obj = employee(Name=name, Salary=salary, Photo = photo,Gender=gender,Designation=designation,Department=department, Head=head1, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
            emp1obj.save()

        elif request.POST.get('designation') == 'Accountant':
            name = request.POST.get('fname')
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            email =request.POST.get("email")
            password= request.POST.get("password")
            passw = make_password(password)
            accobj = accountant(Name=name,Designation=designation,Department=department,Email = email,Password=passw)
            accobj.save()

        else:
            name = request.POST.get("fname")
            photo =request.FILES.get("photo")
            gender = request.POST.get("gender")
            dateofbirth = request.POST.get("DOB")
            address = request.POST.get("address")
            state = request.POST.get("state")
            city = request.POST.get("city")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            head1 = request.POST.get("head")
            pincode = request.POST.get("pincode")
            phoneno = request.POST.get("phone")
            email =request.POST.get("email")
            password= request.POST.get("password")
            salary = request.POST.get('salary')
            passw = make_password(password)
            slugobj = name+'-'+designation
            empobj = employee(Name=name,Salary=salary, Photo = photo,Gender=gender,Designation=designation,Department=department, Head=head1, City = city,DOB = dateofbirth,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw,slug=slugobj)
            empobj.save()
            send_mail = EmailMessage('Login Credentials',f'Dear User {name},\n\nHere are your login credentials:\n\nUsername: {email}\nPassword: {password}.\n\nPlease keep this information confidential and do not share it with others. If you have any questions or need assistance, feel free to contact us.\n\nBest regards,\nAttandance and Payroll Management System',to=['pooja.shekhar21@gmail.com'] )
            send_mail.send()

        return HttpResponse("Customer registered Successfully")
        
#navbar for userpage
def usermain(request):
    return render(request,'usermain.html')

# after userlogin   
def home(request):
    if 'user' in request.session:
        user= request.session.get('user')
        empobj= employee.objects.get(Email=user)
        return render(request, 'index.html', {'user': empobj,'empdetail': empobj})
    

#user profile
def userprofile(request):
    user= request.session['user']
    empobj= employee.objects.get(Email=user)
    return render(request, 'test1.html', {'user': empobj,'empdetail': empobj})

#user edit details    
def editemp(request,slug):
    if request.method =='GET':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        employ = employee.objects.get(slug = slug)
        return render(request,'editform.html',{'user':empobj,'empdetail':employ})
    elif request.method =='POST':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        employ = employee.objects.get(slug = slug)
        employ.Name = request.POST.get('fname')
        employ.Address = request.POST.get('address')
        employ.City = request.POST.get('city')
        employ.State = request.POST.get('state')
        employ.Pincode = request.POST.get('pincode')
        employ.PhoneNo = request.POST.get('phone')
        employ.Email = request.POST.get('email')
        employ.Photo = request.FILES.get('photo')
        employ.save()
        return render(request,'test1.html',{'user':empobj,'empdetail':employ})


#payment cal
def calculation(request):
    user= request.session['user']
    empobj= employee.objects.get(Email=user)
    attobj = attendance.objects.filter(employee=empobj.id)
    
    pcount = 0
    acount = 0
    sal = 0
    sala = 0
    for i in attobj:
        if i.status == 'Present':
            pcount = pcount + 1

        elif i.status == 'Absent':
            acount = acount + 1
    
    salary = empobj.Salary
    sal = salary/(pcount + acount)
    sala = pcount * sal
    countobj = account(present = pcount,absent = acount,employee_id = empobj.id,totalworkingdays=(pcount + acount),paymenttobepaid=sala)
    countobj.save()    
    return empobj,attobj,countobj

#show attendance tabel to useer    
def showattendance(request):
    user= request.session['user']
    empobj= employee.objects.get(Email=user)
    attobj = attendance.objects.filter(employee=empobj.id)
    empobj, attobj, countobj = calculation(request)
    return render(request,'showattendance.html',{'user':empobj,'attobj':attobj,'salary': countobj})

# attendance list at user end
def attendancelist(request):
    if 'user' in request.session:
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        attobj = attendance.objects.filter(employee=empobj.id)
        selected_month = request.GET.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=empobj.id)
        else:
            attobj = attendance.objects.filter(employee_id=empobj.id)

        return render(request,'showattendance.html',{'user':empobj,'attobj':attobj})

#attendance list at hr end   
"""def hrattendancelist(request):
    if request.method== "POST":
        hrs= request.session['hr']
        empobj= hr.objects.get(Email=hrs)
        obj = request.POST['eid']
        print(obj)
        attobj = attendance.objects.filter(employee_id= obj)
        selected_month = request.POST.get('monthFilter')

        if selected_month:
            attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
        else:
            attobj = attendance.objects.filter(employee_id=obj)

        return render(request,'showattendancehr.html',{'hr':empobj,'attobj':attobj})"""

# attendance marking from user end
def attendanceup(request,slug):
    if request.method == 'GET':
        current_time = datetime.now().strftime('%H:%M:%S')   
        print(current_time)
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        empobj = employee.objects.get(slug = slug)
        print(empobj.id)
        return render(request,'attendance.html',{'user':empobj,'empobj1':empobj,'time':current_time})
    elif request.method == 'POST':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        empobj = employee.objects.get(slug = slug)
        emp = request.POST.get('empid')
        date = request.POST.get('date')
        in_time = request.POST.get('intime')
        out_time = request.POST.get('outtime')
        status = request.POST.get('status')
        attobj = attendance(date = date,in_time = in_time , out_time = out_time, employee_id=emp,status=status)
        attobj.save()
        return redirect('../../showattendance/')
        
#attendance update form at hr and head end   
def attendanceuphr(request,slug):
    if 'hr' in request.session:
        if request.method == 'GET':
            current_time = datetime.now().strftime('%H:%M:%S')   
            print(current_time)
            hrs= request.session['hr']
            hrobj= hr.objects.get(Email=hrs)
            empobj = employee.objects.get(slug = slug)
            print(empobj.id)
            return render(request,'attendanceuphr.html',{'hr':hrobj,'empobj1':empobj,'time':current_time})
        elif request.method == 'POST':
            hrs= request.session['hr']
            hrobj= hr.objects.get(Email=hrs)
            empobj = employee.objects.get(slug = slug)
            emp = request.POST.get('empid')
            date = request.POST.get('date')
            in_time = request.POST.get('intime')
            out_time = request.POST.get('outtime')
            status = request.POST.get('status')
            attobj = attendance(date = date,in_time = in_time , out_time = out_time, employee_id=emp,status=status)
            attobj.save()
            url = reverse('showattendance1', args=[empobj.slug])
            return redirect(url)
        
    elif 'head' in request.session:
        if request.method == 'GET':
            current_time = datetime.now().strftime('%H:%M:%S')   
            print(current_time)
            head1= request.session['head']
            hrobj= head.objects.get(Email=head1)
            empobj = employee.objects.get(slug = slug)
            print(empobj.id)
            return render(request,'attendanceuphr.html',{'head':hrobj,'empobj1':empobj,'time':current_time})
        elif request.method == 'POST':
            head1= request.session['head']
            hrobj= head.objects.get(Email=head1)
            empobj = employee.objects.get(slug = slug)
            emp = request.POST.get('empid')
            date = request.POST.get('date')
            in_time = request.POST.get('intime')
            out_time = request.POST.get('outtime')
            status = request.POST.get('status')
            attobj = attendance(date = date,in_time = in_time , out_time = out_time, employee_id=emp,status=status)
            attobj.save()
            url = reverse('showattendance1', args=[empobj.slug])
            return redirect(url)


# calculations for hr end
def calculate_deduction(in_time, out_time, sal_per_day):
    if in_time > '09:15' or out_time < '18:00':
        return sal_per_day / 2
    return 0

def calculation1(request, emp, atobj):
    present_count = 0
    absent_count = 0
    
    for i in atobj:
        if i.status == 'Present':
            present_count += 1

        elif i.status == 'Absent':
            absent_count += 1

    sal_per_day = emp.Salary / 22
    overall_salary = sal_per_day * 22
    print(overall_salary)
    print(f"{sal_per_day} sal per day")

    for i in atobj:
        print(i)

        if i.status == 'Present':
            in_time = i.in_time
            out_time = i.out_time
            deduction = calculate_deduction(in_time, out_time, sal_per_day)
            print(f"{deduction} deducted sal when late")
            overall_salary = overall_salary - deduction
            print(f"{overall_salary} present sal")

        elif i.status == 'Absent':
            overall_salary = overall_salary - sal_per_day
            print(f"{overall_salary} absent sal")

        elif i.status == 'Causal Leave':
            overall_salary = overall_salary - sal_per_day
            print(f"{overall_salary} cl sal")

        elif i.status == 'Paid Leave':
            overall_salary = overall_salary 
            print(f"{overall_salary} pl sal")

        elif i.status == 'Sick Leave':
            overall_salary = overall_salary - (overall_salary*0.3)
            print(f"{overall_salary} sl sal")


    a= overall_salary
    print(f"{a} present absent total sal")

    countobj = account(
        present=present_count,
        absent=absent_count,
        employee_id=emp.id,
        totalworkingdays=present_count + absent_count,
        paymenttobepaid=a
    )
    countobj.save()
    return emp, atobj, countobj

#leave apply from user
def submit_leave_request(request):
    if request.method == 'GET':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        attobj= attendance.objects.filter(employee_id=empobj.id)
        return render(request,'leave_request_form.html',{'user':empobj,'attobj':attobj})
    
    elif request.method == 'POST':
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        attobj= attendance.objects.filter(employee_id=empobj.id)
        in_time = '09:00'
        out_time = '18:00'
        leave_type1 = request.POST.get('leavetype')
        reason2 = request.POST.get('reason1')
        datef = request.POST.get('datefrom')
        datet = request.POST.get('datetill')
        leave_request = LeaveRequest(employee=empobj, leave_type=leave_type1,reason=reason2, datefrom = datef,datetill = datet)
        leave_request.save()
        attobj1 = attendance(date = datef,in_time = in_time , out_time = out_time, employee_id=empobj.id,status=leave_type1)
        attobj1.save()
        return render(request,"showattendance.html",{'user':empobj,'attobj':attobj})

#hr and head can view attendance list
def hrshow(request, slug):
    if 'hr' in request.session:
        if request.method == 'GET':
            hrs= request.session.get('hr')
            hrobj= hr.objects.get(Email=hrs)
            emp= employee.objects.get(slug= slug)
            atobj= attendance.objects.filter(employee_id=emp.id)
            emp, atobj, countobj = calculation1(request,emp,atobj)

            return render(request, 'showattendancehr.html', {'hr': hrobj, 'attobj': atobj, 'salary': countobj,'empobj':emp})
        elif request.method== "POST":
            hrs= request.session['hr']
            empobj= hr.objects.get(Email=hrs)
            emp= employee.objects.get(slug= slug)
            obj = request.POST['eid']
            print(obj)
            atobj = attendance.objects.filter(employee_id= obj)
            selected_month = request.POST.get('monthFilter')

            if selected_month:
                atobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
            else:
                atobj = attendance.objects.filter(employee_id=obj)
            emp, atobj, countobj = calculation1(request,emp,atobj)
            return render(request,'showattendancehr.html',{'hr':empobj,'attobj':atobj,'empobj':emp,'salary':countobj})
        
    elif 'head' in request.session:    
        if request.method == 'GET':
            head1 = request.session.get('head')
            hrobj= head.objects.get(Email=head1)
            emp= employee.objects.get(slug= slug)
            atobj= attendance.objects.filter(employee_id=emp.id)
            return render(request, 'showattendancehr.html',{'head':hrobj,'empobj':emp,'attobj':atobj})
        elif request.method== "POST":
            head1= request.session['head']
            empobj= head.objects.get(Email=head1)
            obj = request.POST['eid']
            print(obj)
            attobj = attendance.objects.filter(employee_id= obj)
            selected_month = request.POST.get('monthFilter')

            if selected_month:
                attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
            else:
                attobj = attendance.objects.filter(employee_id=obj)

            return render(request,'showattendancehr.html',{'head':empobj,'attobj':attobj})

import math
#accountant show
def accshow(request,slug):
    if 'acc' in request.session:
        if request.method == 'GET':
            acc= request.session.get('acc')
            accobj= accountant.objects.get(Email= acc)
            emp= employee.objects.get(slug= slug)
            attobj= attendance.objects.filter(employee_id=emp.id)
            emp, attobj, countobj = calculation1(request,emp,attobj)
            payment1 = math.trunc(countobj.paymenttobepaid)
            print(f"{payment1} payment1")

            return render(request, 'accempdetail.html', {'acc': accobj, 'attobj': attobj, 'salary': countobj,'empobj':emp,'payment':payment1})
        elif request.method== "POST":
            acc= request.session['acc']
            empobj= accountant.objects.get(Email=acc)
            emp= employee.objects.get(slug= slug)
            obj = request.POST['eid']
            print(obj)
            attobj = attendance.objects.filter(employee_id= obj)
            selected_month = request.POST.get('monthFilter')

            if selected_month:
                attobj = attendance.objects.filter(date__month=selected_month,employee_id=obj)
            else:
                attobj = attendance.objects.filter(employee_id=obj)
            emp, attobj, countobj = calculation1(request,emp,attobj)
            payment1 = math.trunc(countobj.paymenttobepaid)
            print(f"{payment1} payment1")
            return render(request,'accempdetail.html',{'acc':empobj,'attobj':attobj,'empobj':emp,'salary':countobj,'payment':payment1})

def update(request, id):
    if 'hr' in request.session:
            hrs= request.session.get('hr')
            hrobj= hr.objects.get(Email=hrs)
            obj = attendance.objects.get(id=id)
            return render(request,'update.html',{'hr':hrobj,'obj':obj})
    
    elif 'head' in request.session:
            head1= request.session.get('head')
            hrobj= head.objects.get(Email=head1)
            obj = attendance.objects.get(id=id)
            return render(request,'update.html',{'head':hrobj,'obj':obj})
    

# for update atndce in hr panel 
def updt(request):
    if 'hr' in request.session:
        if request.method=="POST":
            hrs= request.session.get('hr')
            hrobj= hr.objects.get(Email=hrs)
            dates = request.POST['date']
            print(dates)
            id=  request.POST['id']
            print(id)
            intime = request.POST.get('in_time')
            outtime = request.POST.get('out_time')
            statuss = request.POST.get('status')
            upobj = attendance.objects.get(id=id)
            slugf= upobj.employee.slug
            upobj.date = dates
            upobj.in_time = intime
            upobj.out_time = outtime
            upobj.status = statuss
            upobj.save()
            url= reverse('showattendance1', args=[slugf])
            return redirect(url)
        
    elif 'head' in request.session:
        if request.method=="POST":
            head1= request.session.get('head')
            hrobj= head.objects.get(Email=head1)
            dates = request.POST['date']
            print(dates)
            id=  request.POST['id']
            print(id)
            intime = request.POST.get('in_time')
            outtime = request.POST.get('out_time')
            statuss = request.POST.get('status')
            upobj = attendance.objects.get(id=id)
            slugf= upobj.employee.slug
            upobj.date = dates
            upobj.in_time = intime
            upobj.out_time = outtime
            upobj.status = statuss
            upobj.save()
            url= reverse('showattendance1', args=[slugf])
            return redirect(url)
    
def hrheadhome(request):
    if 'hr' in request.session:
        hrs= request.session['hr']
        hrobj= hr.objects.get(Email=hrs)
        return render(request,'hrheadhome.html',{'hr':hrobj})
    
    elif 'head' in request.session:
        head1 = request.session['head']
        headobj = head.objects.get(Email =head1)
        return render(request,'hrheadhome.html',{'head':headobj})
    
    elif 'acc' in request.session:
        acc = request.session['acc']
        accobj = accountant.objects.get(Email =acc)
        return render(request,'hrheadhome.html',{'head':accobj})
    

#calendar with holiday and leaves to 
def get_holidays(year, country='IN'):
    return holidays.CountryHoliday(country, years=year)


def month_calendar(request, year, month):
    if 'user' in request.session:
        user= request.session['user']
        empobj= employee.objects.get(Email=user)
        attobj = attendance.objects.filter(employee=empobj.id)

        if not (str(year).isdigit() and str(month).isdigit()):
            return HttpResponseBadRequest("Invalid year or month")

        year = int(year)
        month = int(month)

        if not 1 <= month <= 12:
            return HttpResponseBadRequest("Invalid month")

        holidays_set = get_holidays(year)
        leaves = LeaveRequest.objects.filter(
            datefrom__year=year,
            datefrom__month=month,
            datetill__year=year,
            datetill__month=month,
        )

        leave_data = {}
        for leave in leaves:
            leave_data[leave.datefrom.day] = {
                'confirmed': leave.is_approved,
                'reason': leave.reason,
                'leave_type': leave.leave_type,
                'status': 'Approved' if leave.is_approved == 'Approved' else 'Unapproved',
            }
        print(leave_data)

        current_date = datetime(year, month, 1)
        cal = calendar.monthcalendar(year, month)
        month_calendar_html = "<table>"
        month_calendar_html += "<tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>"

        for week in cal:
            month_calendar_html += "<tr>"
            for day in week:
                if day == 0:
                    month_calendar_html += "<td></td>"
                elif day == current_date.day and month == current_date.month and year == current_date.year:
                    leave_info = leave_data.get(day, {})
                    month_calendar_html += f"<td class='today'>{day}"
                    
                    if date(year, month, day) in holidays_set:
                        # Display holiday information
                        holiday_name = holidays_set.get(date(year, month, day), None)
                        month_calendar_html += f"<br><span class='holiday-name'>{holiday_name}</span>"
                    elif leave_info:
                        # Display leave information
                        month_calendar_html += f"<br><span class='leave-status'>{leave_info['status']}</span>"
                    
                    month_calendar_html += "</td>"
                else:
                    is_holiday = date(year, month, day) in holidays_set
                    holiday_name = holidays_set.get(date(year, month, day), None)
                    day_class = 'holiday' if is_holiday else ''
                    day_class += ' sunday' if datetime(year, month, day).weekday() == 6 else ''  # Add 'sunday' class for Sundays
                    month_calendar_html += f"<td class='{day_class}'>{day}"

                    leave_info = leave_data.get(day, {})
                    
                    if leave_info:
                        if leave_info['status'] == 'Approved':
                            month_calendar_html += f"<br><span class='leave-status1'>{leave_info['status']}</span>"
                        elif leave_info['status'] == 'Unapproved':
                            month_calendar_html += f"<br><span class='leave-status'>{leave_info['status']}</span>"

                    if holiday_name:
                        month_calendar_html += f"<br><span class='holiday-name'>{holiday_name}</span>"
                    month_calendar_html += "</td>"
            month_calendar_html += "</tr>"


        month_calendar_html += "</table>"

        # Calculate the next and previous months
        next_month = current_date.replace(day=current_date.day) + timedelta(days=32)
        prev_month = current_date.replace(day=current_date.day) - timedelta(days=1)

        next_month_url = reverse('month_calendar', args=[next_month.year, next_month.month])
        next_month_url += f'?holidays_set={holiday_name}' 
        prev_month_url = reverse('month_calendar', args=[prev_month.year, prev_month.month])
        prev_month_url += f'?holidays_set={holiday_name}'

        # Fetch leave data for the current month
        

    context = {
        'month_calendar': month_calendar_html,
        'next_month': next_month_url,
        'prev_month': prev_month_url,
        'current_date': current_date,
        'leave_data': leave_data,
        'attobj':attobj,
        'user':empobj,
    }

    return render(request, 'calendar.html', context)

def salarypayment(request,tid,empid):
        acc= request.session['acc']
        emp= employee.objects.get(id=empid)

        paymentobj = payment(transactionid = tid, paymentstatus='paid',employee_id=emp.id)
        paymentobj.save()
        
        send_mail = EmailMessage('Order Placed','Order Placed from Paws & Play Store',to=['pooja.shekhar21@gmail.com'] )
        send_mail.send()
        return render(request,'acclogin.html',{'accobj': acc,'payobj': paymentobj})
