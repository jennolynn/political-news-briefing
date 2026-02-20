import feedparser, yaml, datetime, os
from collections import defaultdict

# Get the folder where the script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

# Correct paths relative to script
feeds = load_yaml(os.path.join(BASE_DIR, "feeds.yml"))["sources"]
categories = load_yaml(os.path.join(BASE_DIR, "categories.yml"))["categories"]

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

# Save output to repo root (so Git can commit it)
with open(os.path.join(BASE_DIR, "../daily_briefing.md"), "w") as f:
    f.write(output)
