# WebScrape2GSheets Script

A simple script made to scrape a website and write the data it collects to a Google Sheets document.

## Required modules

To use this script you'll need two modules: Pygsheets (for Google Sheets) and Beautiful Soup 4 - BS4 (for web scraping).

To install these modules use following commands in your terminal: 
```
pip install bs4

pip install pygsheets
```

After the successful installation, you need to enable Sheets API from [google console developers](https://console.developers.google.com/apis?project=turing-booster-178614) page, add credentials and select service account key.
From there follow the instructions and you'll download  a JSON file, rename it to service_creds.json and put it in the folder where the script is located.

That is it, now you can successfully start the script.
