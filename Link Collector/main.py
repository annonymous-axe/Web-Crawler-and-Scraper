# Import libraries
import pandas as pd

from helper_functions import *

import first_depth
import second_depth


def crawl_web(website_url, company_name, rank, depth = 4):

    url = website_url
    all_links = set()

    all_links.add(url)

    # First Depth

    page_links = first_depth.execute(url, window=True)

    all_links.update(page_links)

    df = make_dataframe(website_url, company_name, rank, all_links)

    df.to_excel(f'{rank}_{company_name}.xlsx', index=False)

    print(f"Total Links Collected\t:{len(all_links)}", end="\n")

    ans = 'yes'
    # Second Depth

    for i in range(depth):

        print(f"Depth\t:{i+1}...", end='\n')

        if ans == 'yes':

            df = pd.read_excel(f'{rank}_{company_name}.xlsx')

            all_links = set(df["Page URL"])

            page_links = second_depth.execute(page_links, all_links, window=True)

            all_links.update(page_links)

            print(f"Total Links Collected\t:{len(all_links)}", end="\n")

            df = make_dataframe(website_url, company_name, rank, all_links)

            df.to_excel(f'{rank}_{company_name}.xlsx', index=False)

            ans = input("Do you want to continue ?\t")
        else:
            break

    return all_links

def make_dataframe(website_url, company_name, rank, all_links):
    # Make a DataFrame of links and company detail

    df = pd.DataFrame(columns=["2023 GLOBAL 2000 RANK", "COMPANY NAME", "Website URL", "Page URL"])

    ranks = []
    compony_names = []
    website_urls = []
    page_urls = []

    for link in all_links:
        ranks.append(rank)
        compony_names.append(company_name)
        website_urls.append(website_url)
        page_urls.append(link)

    df["2023 GLOBAL 2000 RANK"] = ranks
    df["COMPANY NAME"] = compony_names
    df["Website URL"] = website_urls
    df["Page URL"] = page_urls

    return df

if __name__ == "__main__":

    website_url = "https://www.shkp.com/en-US"
    company_name = "Sun Hung Kai Properties"
    rank = 459

    main_url = website_url

    
    # Check filter_links function

    common_links = [main_url, "https://facebook.com", "other_links"]
    print("==================================================Filter Links===========================================")
    print(filter_links(common_links))
    print("=========================================================================================================")

    can_continued = input("Url is Correct ?\t:")
    if can_continued == 'yes':
        all_links = crawl_web(website_url, company_name, rank)