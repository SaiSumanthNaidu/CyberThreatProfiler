from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
import json

from collector.models import Feed
from alerts.models import Alert
from nlp_engine.models import Threat


@login_required
def dashboard(request):

    threats = Threat.objects.all()

    high_risk = threats.filter(
        risk_score__gte=70
    ).count()

    medium_risk = threats.filter(
        risk_score__gte=40,
        risk_score__lt=70
    ).count()

    low_risk = threats.filter(
        risk_score__lt=40
    ).count()

    critical_count = Threat.objects.filter(
        risk_score__gte=80
    ).count()

    medium_count = Threat.objects.filter(
        risk_score__gte=40,
        risk_score__lt=80
    ).count()

    low_count = Threat.objects.filter(
        risk_score__lt=40
    ).count()

    recent_alerts = Alert.objects.order_by(
        '-created_at'
    )[:5]

    recent_threats = Threat.objects.order_by(
        '-created_at'
    )[:5]

    category_stats = Threat.objects.values(
        'category'
    ).annotate(
        total=Count('id')
    ).order_by(
        '-total'
    )

    trend_data = Threat.objects.annotate(
        day=TruncDate('created_at')
    ).values(
        'day'
    ).annotate(
        total=Count('id')
    ).order_by('day')

    trend_labels = []
    trend_counts = []

    for item in trend_data:

        trend_labels.append(
            item['day'].strftime('%Y-%m-%d')
        )

        trend_counts.append(
            item['total']
        )

    malware_count = Threat.objects.filter(
        category='Malware'
    ).count()

    phishing_count = Threat.objects.filter(
        category='Phishing'
    ).count()

    data_breach_count = Threat.objects.filter(
        category='Data Breach'
    ).count()

    ddos_count = Threat.objects.filter(
        category='DDoS'
    ).count()

    apt_count = Threat.objects.filter(
        category='APT'
    ).count()

    context = {

        'posts_count': Feed.objects.count(),

        'alerts_count': Alert.objects.count(),

        'threats_count': Threat.objects.count(),

        'high_risk_count': high_risk,

        'critical_count': critical_count,

        'medium_count': medium_count,

        'low_count': low_count,

        'recent_alerts': recent_alerts,

        'recent_threats': recent_threats,

        'category_stats': category_stats,

        'trend_labels': json.dumps(trend_labels),

        'trend_counts': json.dumps(trend_counts),

        'malware_count': malware_count,

        'phishing_count': phishing_count,

        'data_breach_count': data_breach_count,

        'ddos_count': ddos_count,

        'apt_count': apt_count,

        'low_risk': low_risk,

        'medium_risk': medium_risk,

        'high_risk': high_risk,

    }

    return render(
        request,
        'dashboard.html',
        context
    )