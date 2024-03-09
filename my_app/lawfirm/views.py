
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Lawyer, Case, Client

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
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='lawyer').exists():
                return redirect('lawyer_dashboard')
            if user.groups.filter(name='client').exists():
                return redirect('client_dashboard')
           # else:
                # Handle other user groups or a default redirect
               # return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Try Again...")
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
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

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
