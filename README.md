# IMDb Movie Scraper

## Description
This Python script scrapes movie information from IMDb based on a given genre or keyword. It retrieves details such as title, year, IMDb rating, director, cast, and plot summary for each movie.

## Installation
1. Clone the repository or download the script file (`imdb_scraper.py`).
2. Make sure you have Python already install.
3. Install the required libraries using pip:
```sh
pip install requests beautifulsoup4
```

## Usage
1. Run the script by executing the `movie_scraper.py` file with Python. Follow the on-screen prompts to provide the search query, number of pages to scrape, and maximum number of movies to scrape.
```sh
python movie_scrapper.py
```
2. Follow the prompts to enter the genre or keyword to search IMDb, the number of pages to scrape and the number of movies to scrape put zero if want all available movies.
Enter a genre or keyword to search IMDb: action
Enter the number of pages to scrape: 3
Enter the maximum number of movies to scrape (enter 0 for no limit): 10

This will create CSV for 10 movies with action genre.
