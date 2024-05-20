import re
import time

def remove_other_links(links):

    codes = ["calendar", "pdf","ghana", "iraq", "na", "uae", "nl", "uk", "oman", r"\/ar"]#['jo', 'kh', 'la', 'lb', 'mo', 'ph', 'qa', 'se', 'cn','gm', 'jp', 'ae', 'au', 'bd', 'bh', 'bn', 'bw', 'ci', 'cn', 'de', 'fk', 'fr', 'gh', 'gh', 'hk', 'je', 'ke', 'lk', 'mu', 'my', 'ng', 'np', 'pk', 'pl', 'sa', 'sg', 'sl', 'tw', 'tz', 'ug', 'uk', 'us', 'vn', 'za', 'zm', 'zw']
    codes = [r'\b'+code+r'\b' for code in codes]
    new_links = set()

    pattern = '|'.join(codes)
    for link in links:
        if not re.search(pattern, link, flags=re.IGNORECASE):
            new_links.add(link)

    return new_links    

def filter_links(links):
    new_links = set()

    pattern = r'^https:\//\w+\.shkp\.com\/en'
    # pattern = r"nipponsteel\.com"
    other_patterns = r'\/contact\/|\/products\/|\bwebinar\b|subscribe|\bsitemap\b|\bfiles\b|\blit\b|\bja\b|\bstatic-files\b|\btel:\b|\bdeveloper\.\b|\bacademy\b|\bmodels\b|\bdocs\b|direction|@|search|region_page/|form|account|logon|login|sign on|register|signin|signup|download|job|locator|location|document|lang|audio|\.pdf|\.jpg|\.png|\.gif|\.mp3|\.docx|\.zip|\.jpeg|\.exe|\.mp4|\.xml'
    for link in links:

        if re.search(pattern, link, flags=re.IGNORECASE) and not link.endswith('#'):
            if not re.search(other_patterns, link, flags=re.IGNORECASE):
                new_links.add(link)

    new_links = remove_other_links(new_links)
    return new_links

def get_all_links(link, driver, xpath, sleep=2):
    
    driver.get(link)

    time.sleep(sleep)

    hyperlinks = driver.find_elements('xpath', xpath)

    new_links = set()
    
    for hyperlink in hyperlinks:

        link = hyperlink.get_attribute('href')

        # if not re.search('verify|apply|direction|\/global|phone|login|signin|sign-up|signup|logout|download|pdf|shop|product|Country/Region|job|email|submit|subscribe', link, flags=re.IGNORECASE):

        new_links.add(link)

    filtered_links = filter_links(new_links)

    return filtered_links