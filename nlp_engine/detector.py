THREAT_KEYWORDS = {

    'Malware': [
        'malware',
        'trojan',
        'ransomware',
        'virus',
        'worm'
    ],

    'Phishing': [
        'phishing',
        'credential',
        'fake login',
        'email scam'
    ],

    'DDoS': [
        'ddos',
        'botnet',
        'traffic flood'
    ],

    'Data Breach': [
        'data breach',
        'leak',
        'stolen data',
        'database exposed'
    ],

    'APT': [
        'apt',
        'advanced persistent threat'
    ]

}


def detect_threat(text):

    text = text.lower()

    for category, keywords in THREAT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                return category

    return 'Unknown'


def calculate_risk(category):

    scores = {

        'Malware': 85,
        'Phishing': 75,
        'DDoS': 70,
        'Data Breach': 90,
        'APT': 95,
        'Unknown': 20

    }

    return scores.get(
        category,
        20
    )