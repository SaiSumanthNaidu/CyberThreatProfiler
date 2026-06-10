from django.shortcuts import render, redirect, get_object_or_404
from collections import Counter

from .models import Alert


def alert_list(request):

    alerts = Alert.objects.all().order_by(
        '-created_at'
    )

    total_alerts = Alert.objects.count()

    high_count = Alert.objects.filter(
        risk_level='High'
    ).count()

    medium_count = Alert.objects.filter(
        risk_level='Medium'
    ).count()

    low_count = Alert.objects.filter(
        risk_level='Low'
    ).count()

    title_list = []

    for alert in alerts:
        title_list.append(
            alert.title
        )

    title_counter = Counter(
        title_list
    )

    top_alert = "N/A"

    if title_counter:

        top_alert = max(
            title_counter,
            key=title_counter.get
        )

    return render(
        request,
        'alerts.html',
        {
            'alerts': alerts,
            'total_alerts': total_alerts,
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'top_alert': top_alert
        }
    )


def add_alert(request):

    if request.method == "POST":

        Alert.objects.create(
            title=request.POST.get('title'),
            risk_level=request.POST.get('risk_level'),
            description=request.POST.get('description')
        )

        return redirect('alerts')

    return render(
        request,
        'add_alert.html'
    )


def edit_alert(request, id):

    alert = get_object_or_404(
        Alert,
        id=id
    )

    if request.method == "POST":

        alert.title = request.POST.get('title')
        alert.risk_level = request.POST.get('risk_level')
        alert.description = request.POST.get('description')

        alert.save()

        return redirect('alerts')

    return render(
        request,
        'edit_alert.html',
        {
            'alert': alert
        }
    )


def delete_alert(request, id):

    alert = get_object_or_404(
        Alert,
        id=id
    )

    if request.method == "POST":

        alert.delete()

        return redirect('alerts')

    return render(
        request,
        'delete_alert.html',
        {
            'alert': alert
        }
    )