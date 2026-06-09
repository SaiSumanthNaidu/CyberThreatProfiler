from django.shortcuts import render, redirect, get_object_or_404

from .models import Feed

from nlp_engine.detector import (
    detect_threat,
    calculate_risk
)

from nlp_engine.models import Threat

from alerts.models import Alert


def feed_list(request):

    feeds = Feed.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'feed.html',
        {
            'feeds': feeds
        }
    )


def add_feed(request):

    if request.method == "POST":

        description = request.POST.get(
            'description'
        )

        Feed.objects.create(
            source=request.POST.get('source'),
            threat_type=request.POST.get('threat_type'),
            severity=request.POST.get('severity'),
            description=description
        )

        category = detect_threat(
            description
        )

        risk_score = calculate_risk(
            category
        )

        if category != 'Unknown':

            Threat.objects.create(
                threat_name=description[:100],
                category=category,
                risk_score=risk_score
            )

            Alert.objects.create(
                title=f'{category} Threat Detected',
                risk_level='High',
                description=description
            )

        return redirect('feed')

    return render(
        request,
        'add_feed.html'
    )


def edit_feed(request, id):

    feed = get_object_or_404(
        Feed,
        id=id
    )

    if request.method == "POST":

        feed.source = request.POST.get('source')
        feed.threat_type = request.POST.get('threat_type')
        feed.severity = request.POST.get('severity')
        feed.description = request.POST.get('description')

        feed.save()

        return redirect('feed')

    return render(
        request,
        'edit_feed.html',
        {
            'feed': feed
        }
    )


def delete_feed(request, id):

    feed = get_object_or_404(
        Feed,
        id=id
    )

    feed.delete()

    return redirect('feed')