from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import CustomAuthenticationForm  # Import the CustomAuthenticationForm
import pandas as pd



def predict(request):
    return render(request,"predict.html")
# Create your views here.
def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        case_details = request.POST.get('case_details')

        # Unpickle model
        model=pd.read_pickle(r"C:\Users\Hammish Raj Wadeyar\Downloads\new_model.pickle")
        result = model.predict([case_details])
        classification = result[0]

        #PredResults.objects.create(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length,
                                 #  petal_width=petal_width, classification=classification)

        return JsonResponse({'result': classification, 'case_details': case_details },safe=False)
    
def lawyer_data(request):
    return render(request,"lawyer_entry.html")

def lawyer_data_input(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        lawyer_id = float(request.POST.get('lawyer_id'))
        lawyer_name = request.POST.get('lawyer_name')
        specialization = request.POST.get('specialization')
        contact_info = float(request.POST.get('contact_info'))

        

        Lawyer.objects.create(lawyer_id=lawyer_id, lawyer_name=lawyer_name, specialization=specialization,
                                  contact_info=contact_info)

        return JsonResponse({ 'lawyer_id': lawyer_id,
                             'lawyer_name': lawyer_name, 'specialization': specialization, 'contact_info': contact_info},
                            safe=False)
    
def client_data(request):
    return render(request,"client_entry.html")

def client_data_input(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        client_id = float(request.POST.get('client_id'))
        client_name = request.POST.get('lawyer_name')
        address = request.POST.get('address')
        contact_info = float(request.POST.get('contact_info'))
        case_id = float(request.POST.get('case_id'))
        

        Client.objects.create(client_id=client_id, client_name=client_name, address=address,
                                  contact_info=contact_info,case_id=case_id)

        return JsonResponse({ 'client_id': client_id,
                             'client_name': client_name, 'address': address, 'contact_info': contact_info,case_id:'case_id'},
                            safe=False)

def case_data(request):
    return render(request,"entry.html")

def case_data_input(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        case_id = float(request.POST.get('case_id'))
        lawyer_id = float(request.POST.get('lawyer_id'))
        client_id = float(request.POST.get('client_id'))
        case_name = request.POST.get('case_name')

    
        Case.objects.create(case_id=case_id, lawyer_id=lawyer_id, client_id=client_id,case_name=case_name)

        return JsonResponse({ 'case_id': case_id,
                             'lawyer_id': lawyer_id, 'client_id': client_id, 'case_name': case_name},
                            safe=False)

def view_results(request):
    # Submit prediction and show all
    data = {"dataset": Lawyer.objects.all()}
    data1={"dataset": Client.objects.all()}
    data2={"dataset": Case.objects.all()}
    combined_data = {**data, **data1, **data2}
    return render(request, "results.html", combined_data)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))	
            return redirect('login')	



    """if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
             
            if user.groups.filter(name='Lawyer').exists():
                    return redirect('lawyer_dashboard')
            elif user.groups.filter(name='Client').exists():
                    return redirect('client_dashboard')
            else:
                messages.success(request, ("There Was An Error Logging In, Try Again..."))	
                return redirect('login')	
    else:
     
           return render(request, 'login.html', {}) """
    
    """if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if user.customuser.is_lawyer:
                    return redirect('lawyer_dashboard')
                else:
                    return redirect('client_dashboard')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})"""