from django.shortcuts import render
import Database
import os
import json
from web3 import Web3, HTTPProvider



# Create your views here.
def login(request):
    return render(request,'PoliceApp/Login.html')

def logaction(request):
    lid=request.POST['lid']
    password=request.POST['password']

    con=Database.connection()
    cur=con.cursor()
    cur.execute("select * from police where p_id='"+lid+"'and password='"+password+"'")
    d=cur.fetchone()
    print(d)
    if d is not None:
        request.session['pid']=lid
        request.session['station']=d[1]
        request.session['name']=d[2]
        request.session['email']=d[3]
        return render(request,'PoliceApp/PoliceHome.html')
    else:
        context={'msg':'Login Failed..!!'}
        return render(request,'PoliceApp/Login.html',context)

def home(request):
    return render(request,'PoliceApp/ForensicHome.html')

def AddCrimeDetails(request):
    return render(request,'PoliceApp/AddCrimeDetails.html')


global details,tx_receipt
def saveCrimeDetails(data, type):
    global details,contract,tx_receipt

    blockchain_address='http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Crime_SmartContract.json'
    deployed_contract_address = '0xb5eA127DaEc2Ea37E7Dddf11D4f074F5AA155158'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address,abi=contract_abi)
    if type == 'AddCrime':
        details += data
        msg=contract.functions.setData(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)


global rdetails
def readCrimeDetails(contract_type):
    global rdetails
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
        rdetails= contract.functions.getReport().call()


def AddCrimeAction(request):
    global details
    evidence=request.POST['evidence']
    fir_copy=request.POST['fir_copy']
    cno=request.POST['cno']
    type_of_crime=request.POST['type_of_crime']
    data_inc = request.POST['data_inc']
    information = request.POST['Information']
    report = "waiting"
    pid = request.session['pid']
    station = request.session['station']


    readCrimeDetails("AddCrime")
    status='none'
    print(rdetails)
    for dd in rdetails:
        array = dd[1].split("#")
        print(array)
        if array[4] == cno:
            status = "Case Number "+cno+" Already Exist"
            break

    if status == 'none':
        details = ""

        data = pid+"#"+station+"#"+evidence+"#"+fir_copy+"#"+cno+"#"+type_of_crime+"#"+data_inc+"#"+information+"#"+report
        saveCrimeDetails(data, "AddCrime")
        context = {'msg':'Crime Information Added Successful...!!'}
        return render(request,'PoliceApp/AddCrimeDetails.html', context)
    else:
        context = {'msg':'Case No Information Already Exist...!!'}
        return render(request,'PoliceApp/AddCrimeDetails.html', context)

def ViewCrime(request):
    pid = request.session['pid']
    station = request.session['station']

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
            "</tr></thead>"
    readCrimeDetails('AddCrime')

    for dd in rdetails:
        array=dd[1].split("#")
        print(array)
        if array[0] == pid:
            strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                     "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                    "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td><td>"\
                                      "</tr></tbody>"
    strdata += "</table>"
    context = {"data": strdata}
    return render(request,'PoliceApp/ViewCrimeUploads.html',context)


def ViewForensicReport(request):
    pid = request.session['pid']
    station = request.session['station']

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
            "<th scope='col'>Report</th>" \
            "</tr></thead>"
    readCrimeDetails('getReport')

    for dd in rdetails:
        array=dd[1].split("#")
        print(array)
        if array[0] == pid:
            strdata += "<tbody><tr><td>"+str(array[0])+"</td><td>"+str(array[1])+"</td><td>"+str(array[2])+"</td>" \
                                     "<td>"+str(array[3])+"</td><td>"+str(array[4])+"</td><td>"+str(array[5])+"</td>" \
                                    "<td>"+str(array[6])+"</td><td>"+str(array[7])+"</td><td>"+str(array[8])+"</td>"\
                                      "</tr></tbody>"
    strdata += "</table>"
    context = {"data": strdata}
    return render(request,'PoliceApp/ViewForensicReport.html',context)


