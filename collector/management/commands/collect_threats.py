from django.core.management.base import BaseCommand

from collector.models import Feed

from collector.rss_collector import fetch_articles

from nlp_engine.detector import (
    detect_threat,
    calculate_risk
)

from nlp_engine.models import Threat

from alerts.models import Alert


class Command(BaseCommand):

    help = "Collect Threat Intelligence"

    def handle(self, *args, **kwargs):

        articles = fetch_articles()

        for item in articles:

            description = item["description"]

            # Skip duplicates
            if Feed.objects.filter(
                description=description
            ).exists():
                continue

            category = detect_threat(
                description
            )

            risk_score = calculate_risk(
                category
            )

            Feed.objects.create(

                source="RSS Feed",

                threat_type=category,

                severity="High",

                description=description

            )

            if category != "Unknown":

                Threat.objects.create(

                    threat_name=item["title"][:100],

                    category=category,

                    risk_score=risk_score

                )

                if risk_score >= 80:

                    Alert.objects.create(

                        title="Automated Threat Alert",

                        risk_level="High",

                        description=description

                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Threat collection completed"
            )
        )