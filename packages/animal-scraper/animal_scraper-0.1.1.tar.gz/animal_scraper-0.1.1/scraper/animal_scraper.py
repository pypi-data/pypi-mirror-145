#%%
from scraper import AnimalScraper

animal = input('Enter the name of the animal you want to scrape images from: ')
my_scraper = AnimalScraper(animal, headless=False)
my_scraper.get_images()
my_scraper.download_images()

# %%
