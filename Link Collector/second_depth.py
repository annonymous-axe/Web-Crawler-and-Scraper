import undetected_chromedriver as uc

from tqdm import tqdm

from helper_functions import get_all_links

def execute(first_page_links, all_links, x_path = "//a[@href]", window = False):

    second_page_links = set()

    if window:

        driver = uc.Chrome()

    else:

        options = uc.ChromeOptions()

        options.add_argument('--headless')

        driver = uc.Chrome(options=options)

    driver.implicitly_wait(10)

    for link in tqdm(first_page_links):

        try:
            
            links = get_all_links(link, driver, x_path)
            
            second_page_links.update(new_link for new_link in links if new_link not in all_links)
        except:
            continue

    driver.quit()

    return second_page_links