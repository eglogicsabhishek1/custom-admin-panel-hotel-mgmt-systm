from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.apps import apps

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
        print(f"Authenticating user: {username}")
        if user is not None:
            print("Authentication successful. Logging in user.")
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful authentication
        else:
            print("Authentication failed. Invalid credentials.")
            # Authentication failed
            messages.error(request, 'Invalid username or password')
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
    objects = model.objects.all()
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

    if request.method == 'POST':
        # Dynamically create a model form
        form_class = apps.get_model(app_label='backend_ui', model_name=f'{model_name}Form')
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('view_model', model_name=model_name)
    else:
        form_class = apps.get_model(app_label='backend_ui', model_name=f'{model_name}Form')
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
        return redirect('view_model', model_name=model_name)

    return render(request, 'backend_ui/custom/delete.html', {
        'model_name': model_name.capitalize(),
        'cancel_url': 'view_model',
        'cancel_url_kwargs': {'model_name': model_name}
    })

@login_required
def add_model(request, model_name):
    # Dynamically get the model class
    model = apps.get_model(app_label='backend_ui', model_name=model_name)

    if request.method == 'POST':
        # Dynamically create a model form
        form_class = apps.get_model(app_label='backend_ui', model_name=f'{model_name}Form')
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_model', model_name=model_name)
    else:
        form_class = apps.get_model(app_label='backend_ui', model_name=f'{model_name}Form')
        form = form_class()

    return render(request, 'backend_ui/custom/add.html', {
        'form': form,
        'model_name': model_name.capitalize()
    })