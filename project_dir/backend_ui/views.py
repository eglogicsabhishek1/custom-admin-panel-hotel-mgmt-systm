from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.apps import apps
from backend_ui.forms import *
from django.urls import reverse
from django.db import connection

# Updated helper function to reset the primary key sequence for SQLite
def reset_sequence(model):
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        # SQLite-specific sequence reset
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # Authenticate the user using email
        if user is None:
            user = authenticate(request, email=username, password=password)
        
        # Debugging
        if user is not None:
            print("Authentication successful. Logging in user.")
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful authentication
        else:
            # Authentication failed
            # messages.error(request, 'Invalid username or password')
            return render(request, 'backend_ui/admin/login.html', {'error': 'Invalid credentials'})
    
    # Render the login page for GET requests
    return render(request, 'backend_ui/admin/login.html')

@login_required
def home(request):
    # Dynamically fetch all models and filter by app label
    models = [{'name': model._meta.model_name} for model in apps.get_models() if model._meta.app_label == 'backend_ui']
    return render(request, 'backend_ui/admin/home.html', {'models': models})

@login_required
def view_model(request, model_name):
    model = apps.get_model(app_label='backend_ui', model_name=model_name)
    # Retrieves all the records (rows)
    objects = model.objects.all()
    # Extracts the names of all fields (columns)
    fields = [field.name for field in model._meta.fields]
    return render(request, 'backend_ui/custom/view.html', {
        'objects': objects,
        'fields': fields,
        'model_name': model_name.capitalize()
    })

@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('custom_login')
    return render(request, 'backend_ui/admin/logout.html')

@login_required
def edit_model(request, model_name, pk):
    # Dynamically get the model class
    model = apps.get_model(app_label='backend_ui', model_name=model_name)
    instance = get_object_or_404(model, pk=pk)

    # Map model names to their corresponding form classes
    form_classes = {
        'hotel': HotelForm,
        'room': RoomForm,
        'booking': BookingForm,
        'staff': StaffForm,
    }

    form_class = form_classes.get(model_name.lower())
    if not form_class:
        raise LookupError(f"No form class found for model '{model_name}'")

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('view_model', model_name=model_name)
    else:
        form = form_class(instance=instance)

    return render(request, 'backend_ui/custom/edit.html', {
        'form': form,
        'model_name': model_name.capitalize()
    })

@login_required
def delete_model(request, model_name, pk):
    # Dynamically get the model class
    model = apps.get_model(app_label='backend_ui', model_name=model_name)
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        instance.delete()
        reset_sequence(model)  # Reset the sequence after deletion
        return redirect('view_model', model_name=model_name)
    
    cancel_url = reverse('view_model', kwargs={'model_name': model_name})
    
    return render(request, 'backend_ui/custom/delete.html', {
        'model_name': model_name.capitalize(),
        'cancel_url': cancel_url
       
    })

@login_required
def add_model(request, model_name):
    # Dynamically get the model class
    model = apps.get_model(app_label='backend_ui', model_name=model_name)
    
    # Map model names to their corresponding form classes
    form_classes = {
        'hotel': HotelForm,
        'room': RoomForm,
        'booking': BookingForm,
        'staff': StaffForm,
    }

    form_class = form_classes.get(model_name.lower())
    if not form_class:
        raise LookupError(f"No form class found for model '{model_name}'")
    
    if request.method == 'POST':
        # Dynamically create a model form
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            reset_sequence(model)  # Reset the sequence after addition
            # Redirect to the add_room template when the Room model is selected
            if model_name.lower() == 'room':
                return redirect('add_room')
            return redirect('view_model', model_name=model_name)
    else:
        form = form_class()

    return render(request, 'backend_ui/custom/add.html', {
        'form': form,
        'model_name': model_name.capitalize()
    })

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_model', model_name='room')
    else:
        form = RoomForm()

    return render(request, 'backend_ui/custom/room.html', {
        'form': form
    })