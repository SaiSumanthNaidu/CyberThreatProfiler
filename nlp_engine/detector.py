THREAT_KEYWORDS = {

    'Malware': [
        'malware',
        'trojan',
        'ransomware',
        'virus',
        'worm',
        'backdoor',
        'spyware',
        'payload'
    ],

    'Phishing': [
        'phishing',
        'credential',
        'credential theft',
        'fake login',
        'email scam',
        'social engineering'
    ],

    'DDoS': [
        'ddos',
        'botnet',
        'traffic flood',
        'denial of service'
    ],

    'Data Breach': [
        'data breach',
        'leak',
        'stolen data',
        'database exposed',
        'data exposure',
        'compromised records'
    ],

    'APT': [
        'apt',
        'advanced persistent threat',
        'nation-state',
        'state-sponsored'
    ],

    'Vulnerability': [
        'cve',
        'vulnerability',
        'exploit',
        'zero-day',
        'remote code execution',
        'security flaw',
        'authentication bypass',
        'privilege escalation',
        'patch'
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
        'Vulnerability': 80,
        'Unknown': 20

    }

    return scores.get(
        category,
        20
    )