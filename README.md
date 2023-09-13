# One Piece Fandom Scraper
This is a web scraping project that collects character information from the One Piece Fandom website using Scrapy, and can store the data in a PostgreSQL database.

### Project Overview
 - The goal of this project is to scrape character information from the One Piece Fandom website and store it in a PostgreSQL database for further analysis and usage. Since databse creation and credentials are unique I have not activated the pipeline for this, steps for you to store it in a database if you wish will be given.

### Technologies Used
 - Python
 - Scrapy
 - PostgreSQL
 - psycopg2

### Prerequisites
 - Python - I used version 3.11 (install online)
 - PostgreSQL (with appropriate credentials) if you wish to store in database
 - Scrapy (pip install scrapy)
 - psycopg2 (pip install psycopg2)
 - ipython (pip install ipython)
 - Setting Up the Project

### Follow these steps to set up and run the project:
1. Clone the repository
2. Navigate to project directory
3. Create the virtual environment
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment
   ```bash
   venv\Scripts\activate (Windows)
   source venv/bin/activate (Mac/Linux)
   ```
7. Install dependancies
8. Set up PostgreSQL database
   - create a PostgreSQL database
   - configure credentials in pipelines.py under SavingToPostgresPipeline class:
   - ![image](https://github.com/Astr0David/fandom-site-scraper/assets/119695055/ea5a7ece-6c4a-4e7b-93d2-1e4fe76c7fdc)
   - uncomment pipleine in settings.py:
   - ![image](https://github.com/Astr0David/fandom-site-scraper/assets/119695055/4e2f79b8-aa24-4c7f-8321-c77c94ebeea4)

9. Run the scraper in terminal:
  ```bash
   scrapy crawl characterspider
   ```
 - Can also save the content to a json file like this (json file will appear in directory):
 ```bash
   scrapy crawl characterspider -O data.json
   ```
### Screenshots
 - Previous process finishing in terminal then command ready to run scraper again, saving to data.json:
   ![image](https://github.com/Astr0David/fandom-site-scraper/assets/119695055/12a21201-31ef-49eb-83be-4ef280c6f2d5)
 - Data inside database table, seen in pgAdmin4:
   ![image](https://github.com/Astr0David/fandom-site-scraper/assets/119695055/facc03e2-6f3a-44e1-a195-c74180577063)


