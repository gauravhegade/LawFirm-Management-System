from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,DocumentForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Lawyer, Case, Client
import pandas as pd
from django.http import JsonResponse,HttpResponse
from django import forms
from .preprocessing import preprocess_input

import pymongo
"""def login_user(request):
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


	else:
		return render(request, 'login.html', {})"""
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check if the provided username exists in the Lawyer model
        try:
            lawyer_instance = Lawyer.objects.get(lawyer_name=username)
        except Lawyer.DoesNotExist:
            lawyer_instance = None

        # Check if the provided username exists in the Client model
        try:
            client_instance = Client.objects.get(client_name=username)
        except Client.DoesNotExist:
            client_instance = None

        if lawyer_instance:
            # Access cases and clients associated with the lawyer
            lawyer_id = lawyer_instance.lawyer_id
            cases = Case.objects.filter(lawyer_id=lawyer_id)
            clients = Client.objects.filter(case__in=cases)

            # Pass data to the template for lawyer
            context = {
                'lawyer_instance': lawyer_instance,
                'cases': cases,
                'clients': clients,
            }
            return render(request, 'lawyer_dashboard.html', context)

        elif client_instance:
            # Access cases associated with the client
            client_id = client_instance.client_id
            cases = Case.objects.filter(client_id=client_id)

            # Pass data to the template for client
            context = {
                'client_instance': client_instance,
                'cases': cases,
            }
            return render(request, 'client_dashboard.html', context)

        else:
            messages.success(request, "Invalid username or password. Try again.")
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
'''
def lawyer_dashboard(request, lawyer_id):
    # Assuming the lawyer_id is passed as a parameter in the URL

    # Retrieve lawyer information
    lawyer = Lawyer.objects.get(lawyer_id=lawyer_id)

    # Retrieve cases handled by the lawyer
    cases_handled = Case.objects.filter(lawyer_id=lawyer)

    # Retrieve clients associated with the cases
    clients_handled = Client.objects.filter(case_id__in=cases_handled)

    context = {
        'lawyer': lawyer,
        'cases_handled': cases_handled,
        'clients_handled': clients_handled,
    }

    return render(request, 'lawyer_dashboard.html', context)
'''
def predict(request):
    return render(request,"predict.html")
# Create your views here.

def predict_chances(request):
    if request.method == 'POST':
        try:
            print(request.POST.get)
            print("hello")
            specialization = int(request.POST.get('specialization'))
            experience = int(request.POST.get('experience'))
            region = int(request.POST.get('region'))
            X = pd.DataFrame(columns=['Specialization', 'experience', 'region'])
            user_input = pd.DataFrame({
                'Specialization': [specialization],
                'experience': [experience],
                'region': [region]
            }, columns=X.columns) 
            user_input_preprocessed = preprocess_input(user_input)
            model = pd.read_pickle(r"C:\Users\Hammish Raj Wadeyar\Downloads\linear_regression_model.pkl")
            result = model.predict(user_input_preprocessed)
            prediction_result = f"Predicted cost for {specialization} with {experience} years of experience in {region} is {result}."

            # Uncomment the following line if you need to save the predictions to a model
            # PredResults.objects.create(specialization=specialization, experience=experience, region=region, prediction=result)
            print(prediction_result)
            return JsonResponse({'prediction':prediction_result }, safe=False)
        except Exception as e:
            return render(request, 'error_template.html', {'error_message': str(e)})

    # Return a default response if the conditions are not met
    return HttpResponse("Invalid request")

# Create your views here.
def index(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            # Connect to MongoDB
            mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
            mongo_db = mongo_client['Document']

            # Insert document into MongoDB collection
            document_data = {
                "document_id": form.cleaned_data['document_id'],
                "document_type": form.cleaned_data['document_type'],
                "case_id": form.cleaned_data['case_id'],
                "update_date": form.cleaned_data['update_date'].strftime('%Y-%m-%d')
            }
            mongo_db['document.info'].insert_one(document_data)
            mongo_client.close()

            return render(request, 'document.html', {'form': DocumentForm(), 'message': 'Document saved successfully'})
    return render(request, 'document.html', {'form': form})