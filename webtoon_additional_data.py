import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Load the data from the existing Excel file
existing_data = pd.read_excel("webtoons.xlsx")

# Create empty lists to store the additional data
genres = []
authors = []
views = []
subscribes = []
ratings = []
days_updated = []
latest_episodes = []
dates_updated = []
links = []

# Iterate over the rows in the existing data
for index, row in tqdm(existing_data.iterrows(), total=existing_data.shape[0], desc="Processing"):
    link = row["Link"]
    links.append(link)

    # Send a GET request to the link
    response = requests.get(link)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the <h2> element with class "genre" to extract the genre
    genre = soup.find("h2", class_="genre").get_text(strip=True) if soup.find("h2", class_="genre") else None
    genres.append(genre)

    # Find the <h1> element with class "subj" to extract the webtoon title
    title = soup.find("h1", class_="subj").get_text(strip=True) if soup.find("h1", class_="subj") else None

    # Find the <div> element with class "author_area" to extract the author
    author_area = soup.find("div", class_="author_area")
    if author_area:
        author = author_area.get_text(separator=" ", strip=True)
        author = author.replace("author info", "").strip()
    else:
        author = None
    authors.append(author)

    # Find the <ul> element with class "grade_area" to extract view, subscribe, and rating
    grade_area = soup.find("ul", class_="grade_area")
    if grade_area:
        for li in grade_area.find_all("li"):
            span = li.find("span")
            em = li.find("em", class_="cnt")
            if span and em:
                if span.get_text(strip=True) == "view":
                    view_text = em.get_text(strip=True)
                    if "M" in view_text:
                        if "." in view_text:
                            view_text = view_text.replace(".", ",").replace("M", "00,000")
                        else:
                            view_text = view_text.replace("M", ",000,000")
                    views.append(view_text)
                elif span.get_text(strip=True) == "subscribe":
                    subscribe_text = em.get_text(strip=True)
                    if "M" in subscribe_text:
                        if "." in subscribe_text:
                            subscribe_text = subscribe_text.replace(".", ",").replace("M", "00,000")
                        else:
                            subscribe_text = subscribe_text.replace("M", ",000,000")
                    subscribes.append(subscribe_text)
                elif span.get_text(strip=True) == "grade":
                    ratings.append(em.get_text(strip=True))
    else:
        views.append(None)
        subscribes.append(None)
        ratings.append(None)

    # Find the <p> element with class "day_info" to extract the day updated
    day_updated = soup.find("p", class_="day_info").get_text(strip=True) if soup.find("p", class_="day_info") else None
    days_updated.append(day_updated)

    # Find the <li> elements with class "_episodeItem" to extract the latest episode and date updated
    episode_items = soup.find_all("li", class_="_episodeItem")
    if episode_items:
        latest_episode_element = episode_items[0].find("span", class_="subj")
        latest_episode = latest_episode_element.get_text(strip=True) if latest_episode_element else None
        date_updated_element = episode_items[0].find("span", class_="date")
        date_updated = date_updated_element.get_text(strip=True) if date_updated_element else None
    else:
        latest_episode = None
        date_updated = None
    latest_episodes.append(latest_episode)
    dates_updated.append(date_updated)

# Add numbers to the lists
numbers = list(range(1, len(existing_data) + 1))

# Remove specified strings from the "Author" column
authors = [author.replace("author info", "").strip() if author else None for author in authors]

# Create a new DataFrame for the additional data
additional_data = pd.DataFrame({
    "Number": numbers,
    "Link": links,
    "Genre": genres,
    "Author": authors,
    "Views": views,
    "Subscribes": subscribes,
    "Rating": ratings,
    "Day Updated": days_updated,
    "Latest Episode": latest_episodes,
    "Date Updated": dates_updated
})

# Save the additional data DataFrame to a new Excel file
additional_data.to_excel("webtoons_additional_info.xlsx", index=False)
