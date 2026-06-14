from django.shortcuts import render, redirect, get_object_or_404
from collections import Counter
from django.http import HttpResponse
from django.core.management import call_command

from .models import Feed

from nlp_engine.detector import (
    detect_threat,
    calculate_risk
)

from nlp_engine.models import Threat
from alerts.models import Alert

def run_collector(request):
    call_command('collect_threats')
    return HttpResponse("Threat collection completed")

def feed_list(request):

    feeds = Feed.objects.all().order_by(
        '-created_at'
    )

    total_feeds = Feed.objects.count()

    high_count = Feed.objects.filter(
        severity='High'
    ).count()

    medium_count = Feed.objects.filter(
        severity='Medium'
    ).count()

    low_count = Feed.objects.filter(
        severity='Low'
    ).count()

    source_list = []

    for feed in feeds:
        source_list.append(
            feed.source
        )

    source_counter = Counter(
        source_list
    )

    source_labels = list(
        source_counter.keys()
    )

    source_counts = list(
        source_counter.values()
    )

    top_source = "N/A"

    if source_counter:

        top_source = max(
            source_counter,
            key=source_counter.get
        )

    return render(
        request,
        'feed.html',
        {
            'feeds': feeds,
            'total_feeds': total_feeds,
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'top_source': top_source,
            'source_labels': source_labels,
            'source_counts': source_counts
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

            existing_threat = Threat.objects.filter(
                category=category
            ).first()

            if existing_threat:

                existing_threat.occurrence_count += 1
                existing_threat.save()

            else:

                Threat.objects.create(
                    threat_name=description[:100],
                    category=category,
                    risk_score=risk_score,
                    occurrence_count=1
                )

            existing_alert = Alert.objects.filter(
                title=f'{category} Threat Detected'
            ).first()

            if not existing_alert:

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