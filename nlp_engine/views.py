from django.shortcuts import render, redirect, get_object_or_404

from .models import Threat
from collections import Counter

def threat_list(request):

    threats = Threat.objects.all().order_by(
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    )

    risk = request.GET.get(
        'risk',
        ''
    )

    if search:

        threats = threats.filter(
            threat_name__icontains=search
        )

    if risk == "high":

        threats = threats.filter(
            risk_score__gte=80
        )

    elif risk == "medium":

        threats = threats.filter(
            risk_score__gte=60,
            risk_score__lt=80
        )

    elif risk == "low":

        threats = threats.filter(
            risk_score__lt=60
        )

    total_threats = Threat.objects.count()

    high_risk_count = Threat.objects.filter(
        risk_score__gte=80
    ).count()

    malware_count = Threat.objects.filter(
        category='Malware'
    ).count()

    top_category = "N/A"

    category_list = []

    for threat in threats:
        category_list.append(
            threat.category
        )

    category_counter = Counter(
        category_list
    )

    chart_labels = list(
        category_counter.keys()
    )

    chart_counts = list(
        category_counter.values()
    )

    if category_counter:

        top_category = max(
            category_counter,
            key=category_counter.get
        )

    return render(
        request,
        'threats.html',
        {
            'threats': threats,

            'search': search,
            'risk': risk,

            'total_threats': total_threats,
            'high_risk_count': high_risk_count,
            'malware_count': malware_count,
            'top_category': top_category,
            'chart_labels': chart_labels,
            'chart_counts': chart_counts
        }
    )

def threat_detail(request, id):

    threat = get_object_or_404(
        Threat,
        id=id
    )

    return render(
        request,
        'threat_detail.html',
        {
            'threat': threat
        }
    )

def add_threat(request):

    if request.method == "POST":

        Threat.objects.create(
            threat_name=request.POST.get('threat_name'),
            category=request.POST.get('category'),
            risk_score=request.POST.get('risk_score')
        )

        return redirect('threats')

    return render(request, 'add_threat.html')


def edit_threat(request, id):

    threat = get_object_or_404(
        Threat,
        id=id
    )

    if request.method == "POST":

        threat.threat_name = request.POST.get(
            'threat_name'
        )

        threat.category = request.POST.get(
            'category'
        )

        threat.risk_score = request.POST.get(
            'risk_score'
        )

        threat.save()

        return redirect('threats')

    return render(
        request,
        'edit_threat.html',
        {
            'threat': threat
        }
    )


def delete_threat(request, id):

    threat = get_object_or_404(
        Threat,
        id=id
    )

    if request.method == "POST":

        threat.delete()

        return redirect('threats')

    return render(
        request,
        'delete_threat.html',
        {
            'threat': threat
        }
    )