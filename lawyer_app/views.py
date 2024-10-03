from django.shortcuts import render, redirect,get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm,ClientProfileForm,LawyerProfileForm , CaseForm, DocumentUploadForm
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from .models import Lawyer, Case, Client, CustomUser,Document
import pandas as pd
from django.http import JsonResponse,HttpResponse
from django.conf import settings

from .preprocessing import preprocess_input
from django.core.exceptions import PermissionDenied
from pymongo import MongoClient

import gridfs


def info(request):
    if request.method == "GET":
        return render(request,'info.html')
    
@login_required
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
    
@login_required
def search_cases(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        #limit = 5
        cases = None

        if hasattr(request.user, 'lawyer_profile'):
            cases = Case.objects.filter(lawyer=request.user.lawyer_profile, case_name__icontains=query)

        elif hasattr(request.user, 'client_profile'):
            cases = Case.objects.filter(client=request.user.client_profile, case_name__icontains=query)
        
        if cases is not None:
            cases = cases.distinct() #[:limit]
            results = [{'id': case.case_id, 'name': case.case_name} for case in cases]
            return JsonResponse(results, safe=False)
        
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
                            return redirect(reverse('lawyer_app:complete_lawyer_profile')) 
                        else:
                            return redirect(reverse('lawyer_app:lawyer_dashboard'))
                    
                    elif hasattr(user, 'client_profile'):
                        if not user.client_profile.profile_complete:
                            messages.info(request, 'Please complete your client profile.')
                            return redirect(reverse('lawyer_app:complete_client_profile')) 
                        else:
                            return redirect(reverse('lawyer_app:client_dashboard')) 
                    

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

@login_required
def complete_lawyer_profile(request):
    lawyer_profile = request.user.lawyer_profile 
    if request.method == 'POST':
        form = LawyerProfileForm(request.POST, instance=lawyer_profile)
        if form.is_valid():
            form.save()
            lawyer_profile.profile_complete = True  # Mark profile as complete
            lawyer_profile.save()
            messages.success(request, 'Lawyer profile updated successfully.')
            return redirect(reverse('lawyer_app:logout'))  
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
            return redirect(reverse('lawyer_app:logout')) 
    else:
        form = ClientProfileForm(instance=client_profile)
    
    return render(request, 'profile_completion/complete_client_profile.html', {'form': form})

@login_required
def lawyer_dashboard(request):
    lawyer = request.user.lawyer_profile

    cases = Case.objects.filter(lawyer=lawyer, status='approved',is_active=True)

    clients = Client.objects.filter(cases__lawyer=lawyer,cases__status='approved').distinct()  

    context = {
        'lawyer': lawyer,
        'clients': clients,
        'cases': cases,  
        'user':True
    }

    return render(request, 'dashboard/lawyer_dashboard.html', context)

@login_required
def client_profile(request, client_id):

    try:
        client = Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        client = None
    
    context = { 
        'user': True,
        'client' : client
    }
    return render(request, 'profile/client_profile.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('lawyer_app:login'))  

@login_required
def create_case(request):
    if request.method == 'POST':
        print(request.POST)
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.lawyer = request.user.lawyer_profile
            case.status = 'pending'
            case.save()
            return redirect(reverse('lawyer_app:lawyer_dashboard'))
    else:
        form = CaseForm()
    context = {
        'form': form,
        'user': True
    }
    return render(request, 'lawyer/create_case.html', context)

@login_required
def client_dashboard(request):
    client = request.user.client_profile

    active_cases = Case.objects.filter(client=client, is_active=True,status='approved')
    past_cases = Case.objects.filter(client=client, is_active=False)
    
    current_lawyers = Lawyer.objects.filter(cases__client=client, cases__is_active=True, cases__status='approved').distinct()

    past_lawyers = Lawyer.objects.filter(cases__client=client, cases__is_active=False).distinct()
    
    context = {
        'client': client,
        'active_cases': active_cases,
        'past_cases': past_cases,
        'current_lawyers': current_lawyers,
        'past_lawyers': past_lawyers,
        'user': False
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
        'user' : False
    }
    
    return render(request, 'profile/lawyer_profile.html', context)

@login_required
def approve_case(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        case_id = request.POST.get('case_id') 

        try:
            case = Case.objects.get(case_id=case_id, client=request.user.client_profile, status='pending')
        except Case.DoesNotExist:
            case = None
        
        if action == 'approve':
            case.status = 'approved'
            case.save()
        
        elif action == 'reject':
            case.status = 'rejected'
            case.save()

        return redirect(reverse('lawyer_app:approve_case'))

    pending_cases = Case.objects.filter(client=request.user.client_profile, status='pending')
    
    context = {
        'pending_cases': pending_cases,
        'user': False
    }

    return render(request, 'client/approve_case.html', context)

@login_required
def case_status(request):
    lawyer = request.user.lawyer_profile

    if request.method == 'POST':
        action = request.POST.get('action')
        case_id = request.POST.get('case_id')
        if action == 'delete':
            try:
                case = Case.objects.get(case_id=case_id, lawyer=lawyer)
                # case.status='rejected'
                # case.save()
                case.delete()
                messages.success(request, 'Case deleted successfully.')
            except Case.DoesNotExist:
                messages.error(request, 'Case not found.')

    cases = Case.objects.filter(lawyer=lawyer, status__in=['pending', 'rejected'])
    
    context = {
        'cases': cases,
        'user' : True
    }
    
    return render(request, 'lawyer/case_status.html', context)


def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    return render(request, 'errors/500.html', status=500)

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

client = MongoClient(settings.MONGO_URL)
db = client[settings.MONGO_DB]
fs = gridfs.GridFS(db)

@login_required
def upload_document(request):
    status = None
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            case = form.cleaned_data['case']
            
            if (((hasattr(request.user, 'lawyer_profile')) and case.lawyer != request.user.lawyer_profile) and 
                ((hasattr(request.user, 'client_profile')) and case.client != request.user.client_profile)):
                raise PermissionDenied("You do not have permission to upload documents for this case.")
            
            file = request.FILES['file']
            
            file_id = fs.put(file, filename=file.name, contentType=file.content_type)
            document = form.save(commit=False)

            document.gridfs_id = file_id
            document.uploaded_by = request.user
            document.save()
            status = True
            
        else:
            #print("form validation failed") 
            #print(form.errors.as_json())
            status = False
    else:
        form = DocumentUploadForm()

    context = {
        'form': form,
        'status':status,
        'user' : hasattr(request.user, 'lawyer_profile')
    }
    #print(status)
    return render(request, 'upload_document.html', context)


@login_required
def case_details(request, case_id):
    case = get_object_or_404(Case, case_id=case_id)
    if case.status == 'approved':
        client = case.client
        lawyer = case.lawyer
        
        context = {
            'case': case,
            'client': client,
            'lawyer': lawyer,
            'user': hasattr(request.user, 'lawyer_profile')
        }
    else:
        context = {
            'case': None,
            'user': hasattr(request.user, 'lawyer_profile')
            
        }
    return render(request,'case_details.html',context)

@login_required
def fetch_case_documents(request, case_id):
    documents = Document.objects.filter(case_id=case_id)
    document_list = [{
        'id': doc.gridfs_id,
        'filename': doc.filename,
        'uploaded_by': doc.uploaded_by.get_full_name(),
        'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for doc in documents]
    
    return JsonResponse(document_list, safe=False)

# def list_documents(request):
#     files = Document.objects.all()
#     documents = [{'id': file.gridfs_id, 'filename': file.filename} for file in files]
#     return render(request, 'list_documents.html', {'documents': documents})

# @login_required
# def list_documents_by_case(request,case_id):
#     files = Document.objects.filter(case_id=case_id)
#     documents = [{'id': str(file.gridfs_id), 'filename': file.filename} for file in files]
#     return render(request, 'list_documents.html', {'documents': documents})


from bson import ObjectId
@login_required
def download_document(request, file_id):
    file = fs.find_one({"_id": ObjectId(file_id)})
    if file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
        return response
    return HttpResponse('File not found.', status=404)

@login_required
def view_document(request, file_id):
    file = fs.find_one({"_id": ObjectId(file_id)})
    if file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    return HttpResponse('File not found.', status=404)


# Create your views here.
# def index(request):
#     form = DocumentForm()
#     if request.method == 'POST':
#         form = DocumentForm(request.POST)
#         if form.is_valid():
#             # Connect to MongoDB
#             mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
#             mongo_db = mongo_client['Document']

#             # Insert document into MongoDB collection
#             document_data = {
#                 "document_id": form.cleaned_data['document_id'],
#                 "document_type": form.cleaned_data['document_type'],
#                 "case_id": form.cleaned_data['case_id'],
#                 "update_date": form.cleaned_data['update_date'].strftime('%Y-%m-%d')
#             }
#             mongo_db['document.info'].insert_one(document_data)
#             mongo_client.close()

#             return render(request, 'document.html', {'form': DocumentForm(), 'message': 'Document saved successfully'})
#     return render(request, 'document.html', {'form': form})


