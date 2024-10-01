from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,DocumentForm, LoginForm,ClientProfileForm,LawyerProfileForm , CaseForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import Lawyer, Case, Client, CustomUser
import pandas as pd
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from .preprocessing import preprocess_input

import pymongo

def info(request):
    if request.method == "GET":
        return render(request,'info.html')

def search_clients(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')

        clients_by_first_name = Client.objects.filter(user__first_name__icontains=query)

        clients_by_username = Client.objects.filter(user__username__icontains=query)

        clients = clients_by_first_name | clients_by_username
        results = [{'id': client.client_id, 'name': client.user.get_full_name()} for client in clients.distinct()]
        
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse([], safe=False)


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:  
                    login(request, user)

                    if hasattr(user, 'lawyer_profile'):
                        if not user.lawyer_profile.profile_complete:
                            messages.info(request, 'Please complete your lawyer profile.')
                            return redirect('/lawyer/complete-profile')  
                        else:
                            return redirect('/lawyer/dashboard')
                    
                    elif hasattr(user, 'client_profile'):
                        if not user.client_profile.profile_complete:
                            messages.info(request, 'Please complete your client profile.')
                            return redirect('/client/complete-profile') 
                        else:
                            return redirect('/client/dashboard') 
                    

                else:
                    form.add_error(None,'Your account is not active. Please wait for approval.')
            else:
                form.add_error(None,'Invalid username or password.')
        else:
            form.add_error(None,'Invalid username or password.')
            messages.error(request, 'Please correct the errors below.')
        #print(form.non_field_errors().as_json())
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

   
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            role = form.cleaned_data.get('role')

            if role == 'lawyer':
                Lawyer.objects.create(user=user)
            elif role == 'client':
                Client.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please wait for approval.')

            context = {
                'message_head': f"Congratulations, {username}!",
                'message_body': "Your account has been created successfully.",
                'message_title': 'Registration Successful'
            }
            return render(request, 'message.html', context)
        else:
            messages.info(request, f'Account creation failed')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def complete_lawyer_profile(request):
    lawyer_profile = request.user.lawyer_profile 
    if request.method == 'POST':
        form = LawyerProfileForm(request.POST, instance=lawyer_profile)
        if form.is_valid():
            form.save()
            lawyer_profile.profile_complete = True  # Mark profile as complete
            lawyer_profile.save()
            messages.success(request, 'Lawyer profile updated successfully.')
            return redirect('/logout')  
    else:
        form = LawyerProfileForm(instance=lawyer_profile)
    
    return render(request, 'profile_completion/complete_lawyer_profile.html', {'form': form})

@login_required
def complete_client_profile(request):
    client_profile = request.user.client_profile
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client_profile)
        if form.is_valid():
            form.save()
            client_profile.profile_complete = True  # Mark profile as complete
            client_profile.save()
            messages.success(request, 'Client profile updated successfully.')
            return redirect('/logout')  
    else:
        form = ClientProfileForm(instance=client_profile)
    
    return render(request, 'profile_completion/complete_client_profile.html', {'form': form})

@login_required
def lawyer_dashboard(request):
    lawyer = request.user.lawyer_profile

    cases = Case.objects.filter(lawyer=lawyer)

    clients = Client.objects.filter(cases__lawyer=lawyer).distinct()  

    context = {
        'lawyer': lawyer,
        'clients': clients,
        'cases': cases,  
    }

    return render(request, 'dashboard/lawyer_dashboard.html', context)

@login_required
def client_profile(request, client_id):

    try:
        client = Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        client = None
    
    context = { 
        'client' : client,
    }
    return render(request, 'profile/client_profile.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('lawyer_app:login')

@login_required
def create_case(request):
    if request.method == 'POST':
        print(request.POST)
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.lawyer = request.user.lawyer_profile
            case.save()
            return redirect('lawyer_app:lawyer_dashboard')  # Redirect to the dashboard or another page
    else:
        form = CaseForm()
    
    return render(request, 'create_case.html', {'form': form})

@login_required
def client_dashboard(request):
    client = request.user.client_profile

    active_cases = Case.objects.filter(client=client, is_active=True)
    past_cases = Case.objects.filter(client=client, is_active=False)
    
    current_lawyers = Lawyer.objects.filter(cases__client=client, cases__is_active=True).distinct()

    past_lawyers = Lawyer.objects.filter(cases__client=client, cases__is_active=False).distinct()
    
    context = {
        'client': client,
        'active_cases': active_cases,
        'past_cases': past_cases,
        'current_lawyers': current_lawyers,
        'past_lawyers': past_lawyers,
    }
    
    return render(request, 'dashboard/client_dashboard.html', context)

@login_required
def lawyer_profile(request, lawyer_id):
    try:
        lawyer = Lawyer.objects.get(lawyer_id=lawyer_id)
    except Lawyer.DoesNotExist:
        lawyer = None
    
    context = {
        'lawyer': lawyer,
    }
    
    return render(request, 'profile/lawyer_profile.html', context)

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


