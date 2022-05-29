"""
This file contains a bunch of 'back-end' supporting functions. It is meant to
feed data to the UI portion, but doesn't deal with it directly.
"""
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
# TODO: Security stuff we ignore for a demo.
options = Options()
options.headless = True
options.accept_insecure_certs = True
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.headless = True
chromeOptions.accept_insecure_certs = True
chromeOptions.add_argument("--disable-web-security")
chromeOptions.add_argument("--disable-site-isolation-trials")


class YourBrowserSucksError(Exception):
    def __str__(self):
        return "You should get a better browser (our app doesn't work with yours) \n " \
               "https://www.mozilla.org/en-CA/firefox/new/ \n " \
               "https://www.google.com/intl/en_ca/chrome/"


def find_articles(keywords: list[str], browser: str = 'Firefox') -> list[str]:
    """Find and return a list of (plausibly) relevant article URLs given a list of
    search keyword strings. Do this by scraping the web.

    Allow the user to select their preferred browser.
    For now, work only off of the Investopedia website. The rest can come later.
    Also right now I'm only putting in one string for simplicity.

    BE WARNED! WE WEB SCRAPE SO THIS COULD TAKE A WHILE!!!

    >>> find_articles(["Imperial Ships"])
    some links

    >>> find_articles(["Imperial Ships"], 'Chrome')
    some links

    """
    article_links = []
    for keyword in keywords:
        initial_site_url = f'https://www.investopedia.com/search?q={keyword}'

        if browser == 'Firefox':
            driver = webdriver.Firefox(options=options, executable_path='driver (important!)/geckodriver.exe')
        elif browser == 'Chrome':
            driver = webdriver.Chrome(options=chromeOptions, executable_path='driver (important!)/chromedriver.exe')
        else:
            raise YourBrowserSucksError

        # Navigate to our initial site url. Download the source.
        driver.get(initial_site_url)
        srch_res_page = driver.page_source

        # Now parse this thing!
        finance_soup = BeautifulSoup(srch_res_page, 'html.parser')

        # Filter for a particular class that contains article URLs. Make sure they have links.
        search_result_tags = finance_soup.find_all(attrs={'class': "search-results__link mntl-text-link"}, href=True)
        logging.info(f'search result tags: {search_result_tags}')

        # Accumulate their links
        for tag in search_result_tags:
            article_links.append(str(tag['href']))

        driver.__exit__()

    return article_links


def summarize_articles(articles: list[str], browser: str = 'Firefox') -> dict[str, str]:
    """Return a dictionary mapping links of finance articles to their summaries.

    >>> my_links = ['https://www.reuters.com/article/us-tesla-musk-sec/teslas-musk-mocks-sec-as-judge-demands-they-justify-fraud-settlement-idUSKCN1ME2CC',\
    'https://www.investopedia.com/articles/stocks/09/how-interest-rates-affect-markets.asp', \
    'https://www.investopedia.com/investing/how-interest-rates-affect-stock-market/']
    >>> summarize_articles(my_links)
    This is more to check if it runs.
    """
    summaries = {}
    for url in articles:
        summaries[url] = _get_summary(url, browser)

    return summaries


def _get_summary(link: str, browser: str = 'Firefox') -> str:
    """Return an AI-generated summary of an article at a particular link.
    The mean people at summarizebot haven't approved our API Key so this
    function web-scrapes their demo for now.

    This is ethical because the end always justifies the means.

    BE WARNED! WEB-SCRAPING TAKES A WHILE!!!

    >>> _get_summary('https://www.investopedia.com/articles/active-trading/051415/how-why-interest-rates-affect-options.asp')
    A string, obviously.

    >>> _get_summary('https://www.investopedia.com/articles/active-trading/051415/how-why-interest-rates-affect-options.asp', 'Chrome')
    A string, obviously.

    """
    demo_url = 'https://www.summarizebot.com/text_api_demo.html'

    # Choose a good browser
    if browser == 'Firefox':
        driver = webdriver.Firefox(options=options, executable_path='driver (important!)/geckodriver.exe')
    elif browser == 'Chrome':
        driver = webdriver.Chrome(options=chromeOptions, executable_path='driver (important!)/chromedriver.exe')
    else:
        raise YourBrowserSucksError

    # Navigate to their site.
    driver.get(demo_url)

    # Wait 25s if an element hasn't loaded before trying to find it properly.
    driver.implicitly_wait(25)

    # Select the input box and input the link. Wait a bit until it's clickable.
    input_field = driver.find_element(by=By.ID, value='summarization-url')
    WebDriverWait(driver, 10).until(element_to_be_clickable(input_field))
    input_field.send_keys(link)

    # Click the button to summarize, ideally once it's clickable.
    summarize_button = driver.find_element(by=By.ID, value='btnlp')
    WebDriverWait(driver, 10).until(element_to_be_clickable(summarize_button))
    summarize_button.click()

    # Now grab the text! Use the implicit wait to do this after we can find results.
    summarize_results = driver.find_element(by=By.CLASS_NAME, value='demo-sentence')
    summarize_page = driver.page_source
    driver.__exit__()

    # Use BeautifulSoup4 to scrape the sentences together.
    summary_soup = BeautifulSoup(summarize_page, 'html.parser')
    # bruh = summary_soup.find(id='sm-results')
    # no_way = bruh.contents
    summary_tags = summary_soup.find_all(attrs={'class': 'demo-sentence'})

    summary_sentences = []
    for tag in summary_tags:
        # We don't want keywords, those suck.
        if tag.previous_sibling.string != 'Keywords and key phrases':
            summary_sentences.append(tag.string)

    return '\n'.join(summary_sentences)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pass


