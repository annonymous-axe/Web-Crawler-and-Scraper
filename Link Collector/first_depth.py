import undetected_chromedriver as uc

from helper_functions import get_all_links

def execute(main_url, x_path = "//a[@href]", window = False):

    first_page_links = set()

    if window:

        driver = uc.Chrome()

    else:

        options = uc.ChromeOptions()

        options.add_argument('--headless')

        driver = uc.Chrome(options=options)

    driver.implicitly_wait(20) 

    links = get_all_links(main_url, driver, x_path, sleep=12)

    first_page_links.update(links)

    driver.quit()

    return first_page_links