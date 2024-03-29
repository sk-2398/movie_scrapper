import csv
import time
import requests
from bs4 import BeautifulSoup


def scrape_imdb(search_query, num_pages=1, max_movies=None):
    base_url = "https://www.imdb.com"
    search_url = f"{base_url}/search/title/?title={search_query.replace(' ', '+')}&title_type=feature"

    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for page in range(1, num_pages + 1):
        url = f"{search_url}&page={page}"
        time.sleep(1)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        if not movie_items:
            print("No more movies found. Stopping scraping.")
            break
        for movie_item in movie_items:
            movie_info = {}
            try:
                title = movie_item.find('h3', class_='ipc-title__text').text.strip()
                year = movie_item.find('span', class_='dli-title-metadata-item').text.strip()
                rating = movie_item.find('span', class_='ipc-rating-star').text.strip() if movie_item.find('span', class_='ipc-rating-star') else "N/A"
               
                # Movie Detail
                movie_url = base_url + movie_item.find('a', class_='ipc-title-link-wrapper')['href']
                
                movie_response = requests.get(movie_url, headers=headers)
                movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
                director = [director.text.strip() for director in movie_soup.find_all('div', class_='ipc-metadata-list-item__content-container')[0].find_all('a')]
                cast = [actor.text.strip() for actor in movie_soup.find_all('div', class_='sc-bfec09a1-7 gWwKlt')]
                plot_summary = movie_soup.find('div', class_='ipc-html-content-inner-div').text.strip()
                movie_info['Title'] = title
                movie_info['Year'] = year
                movie_info['IMDb Rating'] = rating
                movie_info['Director'] = director
                movie_info['Cast'] = cast
                movie_info['Plot Summary'] = plot_summary
                all_movies.append(movie_info)

                # Limit the number of movies if max_movies is specified
                if max_movies and len(all_movies) >= max_movies:
                    print(f"Maximum number of movies ({max_movies}) reached. Stopping scraping.")
                    break
            except Exception as e:
                print(f"Error occurred while scraping movie information: {str(e)}")
                continue
        if max_movies and len(all_movies) >= max_movies:
            break
    return all_movies

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Year', 'IMDb Rating', 'Director', 'Cast', 'Plot Summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    search_query = input("Enter a genre or keyword to search IMDb: ")
    num_pages = int(input("Enter the number of pages to scrape: "))
    max_movies = int(input("Enter the maximum number of movies to scrape (enter 0 for no limit): "))
    try:
        movies_data = scrape_imdb(search_query, num_pages, max_movies)
        if movies_data:
            save_to_csv(movies_data, f"{search_query}_movies.csv")
            print("Scraping completed successfully!")
        else:
            print("No movies found for the given search query.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
