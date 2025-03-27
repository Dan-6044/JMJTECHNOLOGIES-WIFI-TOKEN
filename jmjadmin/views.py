from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Station
from .forms import StationForm
from django.contrib import messages


def admin_panel(request):
    return render(request, 'dashboard.html')



def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Station added successfully!')
            return redirect('add_station')  # Redirect back to the add_station page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('add_station')

    form = StationForm()
    return render(request, 'add_station.html', {'form': form})


def view_station(request):
    stations = Station.objects.all()  # Retrieve all station records
    return render(request, 'view_station.html', {'stations': stations})

def edit_station(request, id):
    station = get_object_or_404(Station, id=id)
    
    if request.method == 'POST':
        # Get data from the form
        station_code = request.POST['station_code']
        station_name = request.POST['station_name']
        location = request.POST['location']
        station_type = request.POST['station_type']
        status = request.POST['status']

        # Update the station data
        station.station_code = station_code
        station.station_name = station_name
        station.location = location
        station.station_type = station_type
        station.status = status
        station.save()

        # Redirect to the station view or wherever you want
        return redirect('view_station')  # Redirect to the station listing page or wherever

    return render(request, 'view_station.html', {'station': station})


def delete_station(request, id):
    station = get_object_or_404(Station, id=id)
    if request.method == 'POST':  # Confirming deletion with a POST request
        station.delete()
        return redirect('view_station')  # Redirect to the station listing page after deletion
    return render(request, 'confirm_delete_station.html', {'station': station})

@login_required
def hotspots(request):
    return render(request, 'buywifi/hotspots.html')

@login_required
def transactions(request):
    return render(request, 'buywifi/transactions.html')

@login_required
def notifications(request):
    return render(request, 'buywifi/notifications.html')

@login_required
def reports(request):
    return render(request, 'buywifi/reports.html')

@login_required
def analytics(request):
    return render(request, 'buywifi/analytics.html')

@login_required
def billings(request):
    return render(request, 'buywifi/billings.html')

@login_required
def access_control(request):
    return render(request, 'buywifi/access_control.html')

@login_required
def profile_settings(request):
    return render(request, 'buywifi/profile_settings.html')

def logout_view(request):
    logout(request)
    return redirect('login')
