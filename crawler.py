import feedparser
from datetime import datetime
from collections import defaultdict

GOOGLE_NEWS_FEEDS = {
    "Death Threat": "https://news.google.com/rss/search?q=death+threat+received+when:90d&hl=en-IN&gl=IN&ceid=IN:en",
    "Extortion Threat": "https://news.google.com/rss/search?q=extortion+threat+received+when:90d&hl=en-IN&gl=IN&ceid=IN:en",
}

THREAT_KEYWORDS = [
    "death threat", "extortion threat", "threat to kill", "received death threat",
    "received extortion", "got threat", "threat call", "threatened to kill", "murder threat",
    "extortion call", "extortion mail", "extortion message", "extortion messages",
    "extortion voice note", "extortion voice notes", "extortion letter", "extortion email",
    "extortion whatsapp", "threat sms"
]

INDIA_KEYWORDS = [
    "India", "Delhi", "Mumbai", "Punjab", "Uttar Pradesh", "Lucknow", "Noida", "Bihar", "Patna",
    "Kerala", "Tamil Nadu", "Chennai", "Karnataka", "Bangalore", "Andhra Pradesh", "West Bengal",
    "Kolkata", "Rajasthan", "Jaipur", "Gujarat", "Ahmedabad", "Odisha", "Bhubaneswar", "Assam",
    "Haryana", "Chandigarh", "Maharashtra", "Pune", "Nagpur", "Himachal Pradesh", "Shimla",
    "Jammu", "Kashmir", "Srinagar", "Telangana", "Hyderabad", "Chhattisgarh", "Jharkhand",
    "Madhya Pradesh", "Bhopal", "Goa", "Tripura", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Sikkim", "Uttarakhand", "Puducherry", "Ladakh", "Andaman", "Nicobar", "Dadra",
    "Nagar Haveli", "Daman", "Lakshadweep", "Amritsar", "Ludhiana"
]

# Map for detecting medium from title
MEDIUM_KEYWORDS = {
    "phone call": ["phone call", "call", "telephonic", "voice call"],
    "WhatsApp": ["whatsapp", "whatsapp message", "whatsapp call"],
    "SMS": ["sms", "text message"],
    "email": ["email", "mail"],
    "letter": ["letter", "handwritten note"],
    "message": ["message", "texted"],
    "voice note": ["voice note", "audio message"]
}

def is_india_related(text):
    return any(k.lower() in text.lower() for k in INDIA_KEYWORDS)

def is_valid_threat_article(title):
    title_lower = title.lower()
    return any(kw in title_lower for kw in THREAT_KEYWORDS) and is_india_related(title)

def detect_medium(title):
    title_lower = title.lower()
    for medium, keywords in MEDIUM_KEYWORDS.items():
        if any(k in title_lower for k in keywords):
            return medium
    return "Unknown"

def fetch_news():
    all_news = defaultdict(list)
    for category, feed_url in GOOGLE_NEWS_FEEDS.items():
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            source = entry.source.title if hasattr(entry, 'source') else "Unknown"
            pub_date = datetime(*entry.published_parsed[:6]).strftime("%d-%m-%Y")
            
            if is_valid_threat_article(title):
                medium = detect_medium(title)
                all_news[pub_date].append({
                    "title": f"[{category}] {title}",
                    "link": link,
                    "source": source,
                    "medium": medium
                })

    sorted_news = dict(sorted(all_news.items(), key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"), reverse=True))
    return sorted_news
