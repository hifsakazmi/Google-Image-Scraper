# Google Image Scraper
This repo was forked from [Google Image Scraper](https://github.com/ohyicong/Google-Image-Scraper). 
* Added find_image_urls_updated() function to make it work for current google image search DOM (23/01/2025).

## IMPORTANT:
There are still some issues in this code. I might fix those if I had to use this code again but this repo is not being maintained
-----------------------------------------------------------------------------------------------------------------------------
A library created to scrape Google Images.<br>

## Pre-requisites:
1. Google Chrome
2. Python3 packages (Pillow, Selenium, Requests)
3. Windows OS (Other OS is not tested)

## Setup:
1. Open command prompt
2. Clone this repository (or [download](https://github.com/hifsakazmi/Google-Image-Scraper/archive/refs/heads/master.zip))
    ```
    git clone https://github.com/hifsakazmi/Google-Image-Scraper
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Edit your desired parameters in main.py
    ```
    search_keys         = Strings that will be searched for
    number of images    = Desired number of images
    headless            = Chrome GUI behaviour. If True, there will be no GUI
    min_resolution      = Minimum desired image resolution
    max_resolution      = Maximum desired image resolution
    max_missed          = Maximum number of failed image grabs before program terminates. Increase this number to ensure large queries do not exit.
    number_of_workers   = Number of sectioned jobs created. Restricted to one worker per search term and thread.
    ```
4. Run the program
    ```
    python main.py
    ```

## Usage:
To use it, define your desired parameters in main.py and run through the command line:
```
python main.py
```




