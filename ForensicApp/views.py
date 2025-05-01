from django.shortcuts import render

import Database
import json
from web3 import Web3, HTTPProvider

# Create your views here.
def login(request):
    return render(request,'ForensicApp/Login.html')
def register(request):
    return render(request,'ForensicApp/Register.html')

def regaction(request):
    name=request.POST['name']
    email=request.POST['email']
    uname=request.POST['username']
    pwd=request.POST['password']

    #con=pymysql.connect(host='localhost',user='root',password='root',database='forensic_evidence', charset='tuf8')
    con=Database.connection()
    cur1=con.cursor()
    cur1.execute("select * from forensic where email='"+email+"'")
    d=cur1.fetchone()
    print(d)
    if d is not None:
        context={'msg':'Email Already Exist..!!'}
        return render(request,'ForensicApp/Register.html',context)
    else:
        cur=con.cursor()
        i=cur.execute("insert into forensic values(null,'"+name+"','"+email+"','"+uname+"','"+pwd+"','waiting')")
        con.commit()
        if i>0:
            context={'msg':'Registration Successful..!!'}
            return render(request,'ForensicApp/Register.html',context)
        else:
            context={'msg':'Registration Failed..!!'}
            return render(request,'ForensicApp/Register.html',context)

def logaction(request):
    u=request.POST['username']
    p=request.POST['password']

    con=con=Database.connection()
    cur=con.cursor()
    cur.execute("select * from forensic where username='"+u+"'and password='"+p+"'")
    data=cur.fetchone()
    if data is not None:

        status=data[5]
        if status=='waiting':
            context={'msg':'You are not authorized by Admin..!!'}
            return render(request,'ForensicApp/Login.html',context)
        else:
            request.session['id']=data[0]
            request.session['email']=data[2]
            return render(request,'ForensicApp/ForensicHome.html')
    else:
        context={'msg':'Login Failed..!!'}
        return render(request,'ForensicApp/Login.html',context)
def home(request):
    return render(request,'ForensicApp/ForensicHome.html')


global rdetails,reportdetails
def readCrimeDetails(contract_type):
    global rdetails,reportdetails
    rdetails = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Crime_SmartContract.json' #Blockchain SmartContract calling code
    deployed_contract_address = '0xb5eA127DaEc2Ea37E7Dddf11D4f074F5AA155158' #hash address to access Shared Data contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'AddCrime':
        rdetails= contract.functions.getData().call()
    if contract_type == 'getReport':
        reportdetails= contract.functions.getReport().call()


def ViewCrime(request):
    global rdetails
    strdata = "<table class='table'><thead  class='thead-dark'>" \
            "<tr>" \
            "<th scope='col'>Police ID</th>" \
            "<th scope='col'>Station</th>" \
            "<th scope='col'>Evidence</th>" \
            "<th scope='col'>FIR Information</th>" \
            "<th scope='col'>Case NO</th>" \
            "<th scope='col'>Type of Crime</th>" \
            "<th scope='col'>Date of Incident</th>" \
            "<th scope='col'>Info. about police who is handling </th>" \
            "<th scope='col'>Status</th>" \
            "</tr></thead>"
    readCrimeDetails('AddCrime')

    #print(rdetails)
    for dd in rdetails:
        array=dd[1].split("#")
        #print(array)
        if array[8] == "waiting":
            strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                     "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                    "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td>" \
                                   "<td><a href='/fa/GenerateReport?cid="+str(array[4])+"&Pname="+str(array[1])+"'>Generate Report</a></td></td>"\
                                      "</tr></tbody>"
        else:
            strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                     "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                    "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td><td>"+str(array[8])+"</td>"\
                                      "</tr></tbody>"
    strdata += "</table>"
    context = {"data": strdata}
    return render(request,'ForensicApp/ViewCrimeDetails.html',context)


def GenerateReport(request):
    cid=request.GET['cid']
    Pname=request.GET['Pname']
    context = {"cid": cid,'Pname':Pname}
    return render(request,'ForensicApp/AddReport.html',context)


def updateDataBlockChain(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Crime_SmartContract.json' #SmartContract file
    deployed_contract_address = '0xb5eA127DaEc2Ea37E7Dddf11D4f074F5AA155158' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setReport(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def AddFReportAction(request):
    global rdetails
    cid = request.POST['cid']
    pname = request.POST['pname']
    report = request.POST['report']

    readCrimeDetails("AddCrime")

    selected = ""
    print(rdetails)
    for arry in rdetails:
        arrayy = arry[1].split("#")
        print(arrayy[4])
        if arrayy[4] == cid and arrayy[1] == pname:
            selected=arrayy[0]+"#"+arrayy[1]+"#"+arrayy[2]+"#"+arrayy[3]+"#"+arrayy[4]+"#"+arrayy[5]+"#"+arrayy[6]+"#"+arrayy[7]+"#"+report
            updateDataBlockChain(selected)

    strdata = "<table class='table'><thead  class='thead-dark'>" \
            "<tr>" \
            "<th scope='col'>Police ID</th>" \
            "<th scope='col'>Station</th>" \
            "<th scope='col'>Evidence</th>" \
            "<th scope='col'>FIR Information</th>" \
            "<th scope='col'>Case NO</th>" \
            "<th scope='col'>Type of Crime</th>" \
            "<th scope='col'>Date of Incident</th>" \
            "<th scope='col'>Info. about police who is handling </th>" \
            "<th scope='col'>Status</th>" \
            "</tr></thead>"
    readCrimeDetails('AddCrime')

    #print(rdetails)
    for dd in rdetails:
        array=dd[1].split("#")
        strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                     "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                    "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td>" \
                                   "<td><a href='/fa/GenerateReport?cid="+str(array[4])+"&Pname="+str(array[1])+"'>Generate Report</a></td></td>"\
                                      "</tr></tbody>"
    strdata += "</table>"
    context = {"data": strdata,'msg':'Report Generated Successfully...!!'}
    return render(request,'ForensicApp/ViewCrimeDetails.html',context)

def ViewForensicReport(request):
    strdata = "<table class='table'><thead  class='thead-dark'>" \
                "<tr>" \
                "<th scope='col'>Police ID</th>" \
                "<th scope='col'>Station</th>" \
                "<th scope='col'>Evidence</th>" \
                "<th scope='col'>FIR Information</th>" \
                "<th scope='col'>Case NO</th>" \
                "<th scope='col'>Type of Crime</th>" \
                "<th scope='col'>Date of Incident</th>" \
                "<th scope='col'>Info. about police who is handling </th>" \
                "<th scope='col'>Forensic Report</th>" \
                "</tr></thead>"

    readCrimeDetails('getReport')


    for dd in reportdetails:
        array=dd[1].split("#")

        strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                         "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                        "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td><td>"+str(array[8])+"</td>"\
                                          "</tr></tbody>"
    strdata += "</table>"
    context = {"data": strdata}
    return render(request,'ForensicApp/ViewForensicReport.html',context)




