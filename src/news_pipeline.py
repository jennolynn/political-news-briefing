import feedparser, yaml, datetime
from collections import defaultdict

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

feeds = load_yaml("../feeds.yml")["sources"]
categories = load_yaml("../categories.yml")["categories"]

articles = []

for source in feeds:
    feed = feedparser.parse(source["url"])
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.title,
            "summary": entry.get("summary", ""),
            "link": entry.link
        })

categorized = defaultdict(list)

for article in articles:
    text = (article["title"] + article["summary"]).lower()
    for category, rules in categories.items():
        if any(k in text for k in rules["keywords"]):
            categorized[category].append(article)
            break

today = datetime.date.today().isoformat()

output = f"# Daily Political Briefing — {today}\n\n"

for category, items in categorized.items():
    output += f"## {category}\n"
    for a in items[:5]:
        output += f"- **{a['title']}**\n"
    output += "\n"

output += "## Executive Summary\n"
output += (
    "Today’s political news centers on legislative activity in Congress, "
    "ongoing election developments, and executive branch policy actions. "
    "Foreign policy and judicial decisions also continue to shape the national agenda."
)

with open("daily_briefing.md", "w") as f:
    f.write(output)
