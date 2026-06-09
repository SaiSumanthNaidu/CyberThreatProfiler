from django.shortcuts import render, redirect, get_object_or_404

from .models import Threat


def threat_list(request):

    threats = Threat.objects.all().order_by('-created_at')

    return render(
        request,
        'threats.html',
        {
            'threats': threats
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