from flask import Flask, render_template
import requests
import feedparser
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# API KEYS
OPENWEATHER_API_KEY = "2b37afd6afc879f93e17c20aa9212832"
TICKETMASTER_API_KEY = "9L6GR09uz4jvlwGzdBcHu0FNoSvMJEtg"

# Constants
SEATTLE_LAT = 47.6062
SEATTLE_LON = -122.3321
SEATTLE_CITY = "Seattle"
COUNTRY_CODE = "US"

FUN_FACTS = [
    "Seattle is home to the first Starbucks, opened in 1971.",
    "The Space Needle was built for the 1962 World’s Fair.",
    "Seattle has more than 100 public parks within city limits.",
    "The city’s name comes from Chief Si'ahl of the Duwamish tribe.",
    "Seattle is known as the 'Emerald City' due to its lush greenery."
]

FOOD_LIST = [
    {"name": "Canlis", "type": "Fine Dining", "address": "2576 Aurora Ave N",
        "url": "https://www.canlis.com", "image": "img/food/canlis.jpg"},
    {"name": "Beecher's Handmade Cheese", "type": "Cheese", "address": "1600 Pike Pl",
        "url": "https://beechershandmadecheese.com/cafe/pike-place-market/", "image": "img/food/cheese.jpg"},
    {"name": "Pike Place Chowder", "type": "Seafood", "address": "1530 Post Alley",
        "url": "https://www.pikeplacechowder.com", "image": "img/food/chowder.jpg"},
    {"name": "Elliott's Oyster House", "type": "Seafood", "address": "1201 Alaskan Way",
        "url": "https://www.elliottsoysterhouse.com", "image": "img/food/oyster.jpg"},
    {"name": "The Pink Door", "type": "Italian", "address": "1919 Post Alley",
        "url": "https://thepinkdoor.net", "image": "img/food/pink.jpg"},
    {"name": "Theo Chocolate", "type": "Chocolate Factory", "address": "3400 Phinney Ave N",
        "url": "https://www.theochocolate.com", "image": "img/food/theo.jpg"},
    {"name": "Tilikum Place Café", "type": "Breakfast & Brunch", "address": "407 Cedar St",
        "url": "https://www.tilikumplacecafe.com", "image": "img/food/tilikum.jpg"},
    {"name": "Serious Pie", "type": "Pizza", "address": "316 Virginia St",
        "url": "https://www.seriouspieseattle.com/location/serious-pie-downtown/?utm_source=gbp&utm_medium=organic&utm_content=downtown&utm_campaign=fm", "image": "img/food/serious_pie.jpg"},
]

HISTORY_LIST = [
    {
        "title": "Founding of Seattle",
        "image": "img/history/founding.jpg",
        "description": (
            "Seattle was founded in the mid-19th century by pioneers, named after Chief Si'ahl "
            "of the Duwamish and Suquamish tribes. Early settlers established trade and community "
            "in the area, building homes, businesses, and churches. The town quickly became a hub "
            "for logging, shipping, and local governance, laying the foundations for the modern "
            "city we see today. The early collaboration between Native Americans and settlers shaped "
            "Seattle's unique cultural heritage and influenced its growth trajectory."
        ),
        "link": "https://www.historylink.org/File/303#:~:text=Seattle%20was%20founded%20by%20members,Town%20of%20Seattle%22%20became%20official."
    },
    {
        "title": "Klondike Gold Rush",
        "image": "img/history/klondike.jpg",
        "description": (
            "During the late 1890s, Seattle became the gateway to the Klondike Gold Rush, booming "
            "its economy and population as miners stocked up for the journey north. Entrepreneurs, "
            "businesses, and shipping companies flocked to the city, creating jobs and new opportunities. "
            "The influx of wealth helped fund the development of infrastructure, hotels, and entertainment, "
            "cementing Seattle's reputation as the 'Gateway to Alaska.' This period of rapid growth left "
            "lasting impacts on the city’s architecture, commerce, and civic pride."
        ),
        "link": "https://www.nps.gov/klse/learn/historyculture/index.htm"
    },
    {
        "title": "Pioneer Square",
        "image": "img/history/pioneer.jpg",
        "description": (
            "Pioneer Square is Seattle’s oldest neighborhood, showcasing historic architecture, "
            "cobblestone streets, and monuments that tell the story of early settlers. It survived "
            "the Great Fire of 1889, leading to the reconstruction of iconic brick and stone buildings. "
            "Today, it hosts galleries, boutiques, restaurants, and public art installations, serving "
            "as a living museum that reflects Seattle’s resilience, entrepreneurial spirit, and deep "
            "historical roots in the Pacific Northwest."
        ),
        "link": "https://pioneersquare.org/"
    },
    {
        "title": "Tech & Innovation",
        "image": "img/history/tech.jpg",
        "description": (
            "From Boeing to Microsoft and Amazon, Seattle has been at the forefront of technological "
            "innovation, shaping both local and global industries. The city became a hub for aerospace, "
            "software development, e-commerce, and cloud computing, attracting skilled talent from around "
            "the world. This era of innovation transformed Seattle’s economy, urban landscape, and culture, "
            "making it a center for startups, research, and cutting-edge technology that continues to drive "
            "economic growth and global influence today."
        ),
        "link": "https://www.britannica.com/place/Seattle-Washington/Economy"
    },
    {
        "title": "Waterfront & Shipping",
        "image": "img/history/water.jpg",
        "description": (
            "Seattle’s waterfront has been crucial for trade, shipping, and fishing, connecting the city "
            "to global markets and supporting its maritime heritage. The piers, warehouses, and shipping "
            "infrastructure enabled the export of lumber, seafood, and goods while attracting tourists and "
            "local commerce. Over time, the waterfront evolved into a cultural and recreational hub, featuring "
            "parks, restaurants, and public spaces, reflecting both the city’s economic history and its ongoing "
            "connection to the waters that define the region."
        ),
        "link": "https://mohai.org/blog/2025/from-indigenous-crossroads-to-urban-promenade-the-evolving-history-of-seattles-waterfront/"
    }
]

ATTRACTIONS_LIST = [
    {
        "title": "Pike Place Market",
        "image": "img/attractions/pike.jpg",
        "description": "Seattle’s iconic market, famous for fresh seafood, crafts, and the flying fish. A must-visit for locals and tourists.",
        "address": "85 Pike St",
        "link": "https://www.pikeplacemarket.org/"
    },
    {
        "title": "Space Needle",
        "image": "img/attractions/space_needle.jpg",
        "description": "The symbol of Seattle’s skyline. Enjoy panoramic city views and the rotating restaurant at the top.",
        "address": "400 Broad St",
        "link": "https://www.spaceneedle.com/"
    },
    {
        "title": "Chihuly Garden and Glass",
        "image": "img/attractions/chihuly.jpg",
        "description": "Experience the breathtaking glass sculptures of artist Dale Chihuly. A vibrant mix of art and nature.",
        "address": "305 Harrison St",
        "link": "https://www.chihulygardenandglass.com/"
    },
    {
        "title": "Seattle Aquarium",
        "image": "img/attractions/aquarium.jpg",
        "description": "Discover marine life native to the Pacific Northwest, including sea otters, octopuses, and local fish species.",
        "address": "1483 Alaskan Way",
        "link": "https://www.seattleaquarium.org/"
    },
    {
        "title": "Kerry Park",
        "image": "img/attractions/kerry.jpg",
        "description": "Capture the iconic view of Seattle’s skyline with Mount Rainier in the background from this small hillside park.",
        "address": "211 W Highland Dr",
        "link": "https://www.seattle.gov/parks/find/parks/kerry-park"
    },
    {
        "title": "Museum of Pop Culture",
        "image": "img/attractions/pop.jpg",
        "description": "Step into Seattle’s Museum of Pop Culture and explore immersive exhibits celebrating music, movies, gaming, and the icons who shaped our culture.",
        "address": "325 5th Ave N",
        "link": "https://www.mopop.org/"
    },
]
ACTIVITIES_LIST = [
    {
        "title": "Ballard Kayak & Paddleboard Tours",
        "image": "img/things_to_do/kayak.jpg",
        "description": "Paddle through the heart of Seattle, enjoy city views from the water, and spot local wildlife on Lake Union.",
        "address": "7901 Seaview Ave NW",
        "link": "https://www.ballardkayak.com/"
    },
    {
        "title": "Seattle Great Wheel",
        "image": "img/things_to_do/wheel.jpg",
        "description": "Ride this iconic Ferris wheel on the waterfront for breathtaking views of the city and Elliott Bay.",
        "address": "1301 Alaskan Wy",
        "link": "https://seattlegreatwheel.com/"
    },
    {
        "title": "Bill Speidel’s Underground Tour",
        "image": "img/things_to_do/underground.jpg",
        "description": "Discover Seattle’s hidden underground streets and hear fascinating stories about the city’s history.",
        "address": "614 1st Ave",
        "link": "https://undergroundtour.com/"
    },
    {
        "title": "Olympic Sculpture Park",
        "image": "img/things_to_do/olympic.jpg",
        "description": "Explore contemporary sculptures in a beautiful waterfront park with trails and public art installations.",
        "address": "2901 Western Avenue",
        "link": "https://www.seattleartmuseum.org/visit/olympic-sculpture-park"
    },
    {
        "title": "Ballard Locks",
        "image": "img/things_to_do/ballard.jpg",
        "description": "Watch boats pass through the locks, see salmon at the fish ladder, and enjoy nearby walking trails.",
        "address": "3015 NW 54th St",
        "link": "https://ballardlocks.org/"
    },
    {
        "title": "Gas Works Park",
        "image": "img/things_to_do/gas.jpg",
        "description": "Relax at this unique park with panoramic city views, remnants of an old gas plant, and open spaces for picnics.",
        "address": " 2101 N Northlake Way",
        "link": "https://www.seattle.gov/parks/allparks/gas-works-park"
    },
    {
        "title": "Ferry to Bainbridge Island",
        "image": "img/things_to_do/ferry.jpg",
        "description": "Take a scenic ferry ride across Puget Sound and explore Bainbridge Island’s shops, parks, and waterfront.",
        "address": "801 Alaskan Wy",
        "link": "https://www.bainbridgeisland.com/ferry/"
    },
    {
        "title": "Discovery Park Trails",
        "image": "img/things_to_do/discovery_park.jpg",
        "description": "Hike through Seattle’s largest green space, featuring forested trails, beaches, and stunning views of Puget Sound.",
        "address": "3801 Discovery Park Blvd",
        "link": "https://www.wta.org/go-hiking/hikes/discovery-park-loop-trail"
    },
    {
        "title": "Fremont Troll & Neighborhood Walk",
        "image": "img/things_to_do/fremont_troll.jpg",
        "description": "Explore Seattle’s Fremont neighborhood, see the iconic Fremont Troll under the Aurora Bridge, and enjoy a leisurely walk through Fremont and Ballard with local shops, murals, and scenic streets.",
        "address": "North 36th Street, Troll Ave N",
        "link": "https://www.gpsmycity.com/tours/fremont-neighborhood-walking-tour-2598.html"
    },
]


# --- Functions ---

def fetch_ticketmaster_events(segment_name=None, exclude_segment=None):
    now = datetime.utcnow()
    end_date = now + timedelta(days=60)
    start_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = (
        f"https://app.ticketmaster.com/discovery/v2/events.json"
        f"?apikey={TICKETMASTER_API_KEY}"
        f"&city={SEATTLE_CITY}"
        f"&countryCode={COUNTRY_CODE}"
        f"&startDateTime={start_iso}"
        f"&endDateTime={end_iso}"
        f"&size=100"
        f"&sort=date,asc"
    )

    if segment_name:
        url += f"&segmentName={segment_name}"

    events = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "_embedded" in data and "events" in data["_embedded"]:
            for event in data["_embedded"]["events"]:
                classifications = event.get("classifications", [{}])
                segment = classifications[0].get("segment", {}).get(
                    "name") if classifications else None

                if exclude_segment and segment == exclude_segment:
                    continue

                name = event.get("name", "No title")
                event_url = event.get("url", "#")
                dates = event.get("dates", {}).get("start", {})
                local_date = dates.get("localDate", "TBA")
                local_time = dates.get("localTime", "00:00:00")
                venues = event.get("_embedded", {}).get("venues", [{}])
                venue_name = venues[0].get("name", "Unknown venue") if venues else "Unknown venue"

                events.append({
                    "title": name,
                    "url": event_url,
                    "date": local_date,
                    "time": local_time,
                    "venue": venue_name
                })
    except Exception as e:
        print("Ticketmaster API error:", e)

    future_events = []
    for e in events:
        event_datetime_str = f"{e['date']} {e['time'] or '00:00:00'}"
        try:
            event_dt = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            event_dt = now
        if event_dt >= now:
            future_events.append(e)

    future_events.sort(key=lambda e: datetime.strptime(
        f"{e['date']} {e['time'] or '00:00:00'}", "%Y-%m-%d %H:%M:%S"))
    return future_events

# --- Routes ---


@app.route("/")
def index():
    fact = random.choice(FUN_FACTS)
    return render_template("index.html", fun_fact=fact)


@app.route("/weather")
def weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={SEATTLE_LAT}&lon={SEATTLE_LON}&appid={OPENWEATHER_API_KEY}&units=imperial"
    weather = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = {
            "city": SEATTLE_CITY,
            "temperature": data.get("main", {}).get("temp", "N/A"),
            "description": data.get("weather", [{}])[0].get("description", "N/A").title(),
            "icon": data.get("weather", [{}])[0].get("icon", ""),
        }
    except Exception as e:
        print("Weather API error:", e)

    current_date = datetime.now().strftime("%A, %B %d, %Y")
    return render_template("weather.html", weather=weather, current_date=current_date)


@app.route("/events")
def events():
    event_list = fetch_ticketmaster_events(exclude_segment="Sports")
    if not event_list:
        event_list = [{"title": "No upcoming events found.",
                       "url": "#", "date": "", "time": "", "venue": ""}]
    return render_template("events.html", events=event_list)


@app.route("/sports")
def sports():
    sports_categories = ["Seahawks", "Mariners", "Sounders", "UW Huskies", "Other Sports"]
    sports_data = {cat: [] for cat in sports_categories}
    now = datetime.utcnow()
    end_date = now + timedelta(days=60)
    start_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = (
        f"https://app.ticketmaster.com/discovery/v2/events.json?"
        f"apikey={TICKETMASTER_API_KEY}&city={SEATTLE_CITY}&countryCode={COUNTRY_CODE}"
        f"&classificationName=sports&startDateTime={start_iso}&endDateTime={end_iso}&size=200&sort=date,asc"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "_embedded" in data and "events" in data["_embedded"]:
            for event in data["_embedded"]["events"]:
                name = event.get("name", "")
                link = event.get("url", "#")
                date = event.get("dates", {}).get("start", {}).get("localDate", "TBA")
                time = event.get("dates", {}).get("start", {}).get("localTime", "")
                venue = event.get("_embedded", {}).get("venues", [{}])[
                    0].get("name", "Unknown venue")

                emoji = "🏟"
                lower_name = name.lower()
                if "seahawks" in lower_name:
                    category = "Seahawks"
                    emoji = "🏈"
                elif "mariners" in lower_name:
                    category = "Mariners"
                    emoji = "⚾"
                elif "sounders" in lower_name:
                    category = "Sounders"
                    emoji = "⚽"
                elif "huskies" in lower_name or "washington" in lower_name:
                    category = "UW Huskies"
                else:
                    category = "Other Sports"

                event_info = {"title": name, "url": link, "date": date,
                              "time": time, "venue": venue, "emoji": emoji}
                sports_data[category].append(event_info)

    except Exception as e:
        print("Sports API error:", e)

    for category in sports_data:
        filtered = []
        for e in sports_data[category]:
            try:
                dt = datetime.strptime(
                    f"{e['date']} {e['time'] or '00:00:00'}", "%Y-%m-%d %H:%M:%S")
                if dt >= now:
                    filtered.append(e)
            except ValueError:
                filtered.append(e)
        sports_data[category] = sorted(filtered, key=lambda x: x["date"])

    return render_template("sports.html", sports_data=sports_data)


@app.route("/news")
def news():
    rss_urls = [
        "https://www.seattletimes.com/feed/",
        "https://komonews.com/rss",
        "https://www.kiro7.com/rss/",
        "https://news.google.com/rss/search?q=Seattle&hl=en-US&gl=US&ceid=US:en"
    ]
    articles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:9]:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "published": entry.get("published", "No date"),
                "source": feed.feed.get("title", "Seattle News")
            })

    def sort_key(article):
        try:
            return feedparser.parse(article["published"]).updated_parsed
        except Exception:
            return (1970, 1, 1, 0, 0, 0, 0, 0, 0)
    articles.sort(key=sort_key, reverse=True)
    return render_template("news.html", articles=articles)


@app.route("/food")
def food():
    return render_template("food.html", food_list=FOOD_LIST)


@app.route("/history")
def history():
    return render_template("history.html", history_list=HISTORY_LIST)


@app.route("/attractions")
def attractions():
    return render_template("attractions.html", attractions_list=ATTRACTIONS_LIST)


@app.route("/things-to-do")
def things_to_do():
    return render_template("things_to_do.html", activities_list=ACTIVITIES_LIST)


if __name__ == "__main__":
    app.run(debug=True)
