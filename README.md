# Seattle Now
#### Video Demo: <https://youtu.be/ZfCGxcS0s_0>
#### Description:
Seattle Now is a web application built with Flask that aggregates essential Seattle information in one place. It provides current weather, upcoming events, sports schedules and results, news headlines, and a list of popular attractions. The app is designed for both locals and tourists who want a quick and easy way to see what’s happening in the city and plan their day.

The project demonstrates how to integrate multiple APIs into a single web platform and emphasizes responsive, user-friendly design. Each section of the app is designed to display data clearly, with interactive features such as filtering events by category and dynamically updating weather backgrounds.

---

## Features

- **Weather:** Displays current conditions and a short forecast. The background dynamically changes based on the weather (sunny, rainy, cloudy, etc.), providing visual cues about Seattle’s climate.
- **Events:** Shows upcoming events with dates, categories, and links to more information. Users can filter by category to quickly find concerts, festivals, or local activities.
- **Sports:** Lists recent and upcoming games for Seattle teams, including scores and schedules.
- **News:** Aggregates local Seattle news from reliable sources, giving users quick access to important headlines.
- **Attractions & Activities:** Offers a curated list of museums, parks, and other must-visit places for visitors and locals.

---

## Project Architecture

- **Frontend:** HTML templates with Jinja2, responsive CSS, and minimal JavaScript for interactivity. Each page extends a `base.html` template to maintain a consistent layout and navbar.
- **Backend:** Python with Flask, which handles routing, API calls, and data formatting before rendering templates. The backend ensures that data from different sources is presented consistently.
- **Deployment:** Hosted on Render, with a configuration to launch via Gunicorn. The app can also be run locally for testing with Flask’s built-in server.
- **Data Sources:** The app integrates multiple APIs:
  - Weather API (OpenWeather or similar)
  - News API (Seattle-focused news source)

---

## File Structure
