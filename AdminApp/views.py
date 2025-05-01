from django.shortcuts import render
import Database
from ForensicEvidence.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
import random
import string
# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'AdminApp/Login.html')

def logaction(request):
    u=request.POST['username']
    p=request.POST['password']

    if u=='Admin' and p=='Admin':
            return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Login Failed..!!'}
        return render(request,'AdminApp/Login.html',context)
def home(request):
    return render(request,'AdminApp/AdminHome.html')

def ViewForensic(request):
    tabledata="<table class='table' style='margin-bottom:100px'>" \
              "<thead class='thead-dark'><tr><th scope='col'>Name</th><th scope='col'>Email</th><th scope='col'>Status</th></tr>"
    con=Database.connection()
    cur=con.cursor()
    cur.execute("select * from forensic")
    data=cur.fetchall()
    for d in data:
        id=str(d[0])
        status=d[5]
        if status=='waiting':
            tabledata+="<tr><td scope='row'>"+str(d[1])+"</td><td>"+str(d[2])+'</td><td><a href=\'Accept?id='+id+'\'>Click</a></td></tr>'
        else:
            tabledata+="<tr><td scope='row'>"+str(d[1])+"</td><td>"+str(d[2])+'</td><td>Authorized</td></tr>'
    tabledata+="</table>"
    context={'data':tabledata}
    return render(request,'AdminApp/ViewForensic.html',context)

def Accept(request):
    fid=request.GET['id']
    con=Database.connection()
    cur=con.cursor()
    cur.execute("update forensic set status='Authorized' where id='"+fid+"'")
    con.commit()
    tabledata="<table class='table' style='margin-bottom:100px'>" \
              "<thead class='thead-dark'><tr><th scope='col'>Name</th><th scope='col'>Email</th><th scope='col'>Status</th></tr>"
    cur1=con.cursor()
    cur1.execute("select * from forensic")
    data=cur1.fetchall()
    for d in data:
        id=str(d[0])
        status=d[5]
        if status=='waiting':
            tabledata+="<tr><td scope='row'>"+str(d[1])+"</td><td>"+str(d[2])+'</td><td><a href=\'Accept?id='+id+'\'>Click</a></td></tr>'
        else:
            tabledata+="<tr><td scope='row'>"+str(d[1])+"</td><td>"+str(d[2])+'</td><td>Authorized</td></tr>'
    tabledata+="</table>"
    context={'data':tabledata}
    return render(request,'AdminApp/ViewCrimeUploads.html',context)




def AddPolice(request):
    random_6_digit = random.randint(100000, 999999)

    context={'no':random_6_digit}
    return render(request,'AdminApp/AddPolice.html',context)

def AddPction(request):
    pid=request.POST['pid']
    station=request.POST['station']
    name=request.POST['name']
    email=request.POST['email']
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    con=Database.connection()
    cur=con.cursor()
    cur.execute("insert into police values(null,'"+station+"','"+name+"','"+email+"','"+pid+"','"+password+"')")
    con.commit()
    #email settings
    subject = "LOGIN DETAILS"
    text_content = ""
    html_content = "<table border='1'><tr><th style='background:black;color:white'>Assign Station</th>" \
                   "<th style='background:black;color:white'>Login ID</th>" \
                   "<th style='background:black;color:white'>Login Password</th></tr><tr><td>"+station+"</td><td>"+pid+"</td><td>"+password+"</td></tr></table>"
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [email]
    # if send_mail(subject,message,from_mail,to_mail):
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
    msg.attach_alternative(html_content, "text/html")
    if msg.send():
        sts = 'sent'
        print(sts)
    random_6_digit = random.randint(100000, 999999)

    context={"msg":"Police Added Successfully..!!",'no':random_6_digit}
    return render(request,'AdminApp/AddPolice.html',context)

def ViewPolice(request):
    tabledata="<table  class='table'><thead class='thead-dark'>" \
              "<tr><th scope='col'>Police Station</th>" \
              "<th scope='col'>Name</th>" \
              "<th scope='col'>Email</th>" \
              "<th scope='col'>Police ID</th></thead></tr>"
    con=Database.connection()
    cur=con.cursor()
    cur.execute("select * from police")
    data=cur.fetchall()
    for d in data:
        tabledata+="<tr><td scope='row'>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    tabledata+="</table>"
    context={'data':tabledata}
    return render(request,'AdminApp/ViewPolice.html',context)
