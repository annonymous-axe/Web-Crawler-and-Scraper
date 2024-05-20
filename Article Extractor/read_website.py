
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def get_text(df, keywords):

    ranks = []
    company_names = []
    main_urls = []
    urls = []
    find_texts = []
    find_keywords = []

    all_links = df["Page URL"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    count = 0
    for link in tqdm(all_links):

        try:
            
            response = requests.get(link, headers=headers, timeout=5)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove header, footer, and navigation bar elements
                for header in soup(['header', 'footer', 'nav']):
                    header.decompose()
        
                for word in keywords:
                    texts = set()
                    keywordses = set()
                    
                    # Extract text from various tags
                    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'tr', 'li', 'a']):
                        if tag.string and re.search(r'\b'+word+r'\b', tag.string, flags=re.IGNORECASE):
                            texts.add(tag.string.strip())
                    
                    if len(texts) > 0:
                        count += 1
                        ranks.append(df['2023 GLOBAL 2000 RANK'][0])
                        company_names.append(df['COMPANY NAME'][0])
                        main_urls.append(df['Website URL'][0])
                        urls.append(link)
                        find_texts.append(', '.join(texts))
                        
                        keywordses.update([word for word in keywords if re.search(r'\b'+word+r'\b', ', '.join(texts), flags=re.IGNORECASE)])
                        find_keywords.append(', '.join(keywordses))
                        print("Total Entries\t:", count)

            # else:
            #     print(response)
            #     print("Link\t:", link)
                # break

        except Exception as e:
            print(e)
            continue

    result = pd.DataFrame(columns=['2023 GLOBAL 2000 RANK', 'COMPANY NAME', 'Website URL', 'Keywords', 'Text','Page URL'])

    result['2023 GLOBAL 2000 RANK'] = ranks
    result['COMPANY NAME'] = company_names
    result['Website URL'] = main_urls
    result['Page URL'] = urls
    result['Keywords'] = find_keywords
    result['Text'] = find_texts

    return result    