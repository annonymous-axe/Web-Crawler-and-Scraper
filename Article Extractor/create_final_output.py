import pandas as pd

import re

def save_final_output(company_name):

    output_folder = "Output Files/"
    output_path = output_folder+company_name    

    result_df = pd.read_excel(output_path)

    keywords = set()
    with open('keywords.txt') as file:
        keywords.update(file.readlines())

    keywords = [word.replace('\n', '').strip() for word in keywords]

    contextual_words = set()
    with open('Contextual Words.txt') as file:
        contextual_words.update(file.readlines())

    contextual_words = [word.replace('\n', '') for word in contextual_words]

    present_contextual_words = []

    for text in result_df['Text']:
        words = set()
        for word in contextual_words:
            if re.search(r'\b'+word+r'\b', text, flags=re.IGNORECASE):
                words.add(word)

        if len(words) > 0:
            present_contextual_words.append(', '.join(words))

        else:
            present_contextual_words.append('N/A')

    contextual_words_df = {'Contextual Words': present_contextual_words}
    full_result = pd.concat([result_df, pd.DataFrame.from_dict(contextual_words_df)], axis=1)

    present_kewords = set()
    left_keywords = set()
        
    for word in result_df['Keywords']:
        present_kewords.update(word.strip() for word in word.split(','))

    for word in keywords:
        if word not in present_kewords:
            left_keywords.add(word)

    new_row = {
        '2023 GLOBAL 2000 RANK': [result_df['2023 GLOBAL 2000 RANK'][0]], 
        'COMPANY NAME' : [result_df['COMPANY NAME'][0]],
        'Keywords' :[', '.join(left_keywords)],
        'Contextual Words': ['N/A'],
        'Page URL' : ['N/A'],
        'Text' : ['N/A'],
        'Website URL' : [result_df['Website URL'][0]]
    }

    full_result = pd.concat([full_result, pd.DataFrame(new_row)], axis=0, ignore_index=True)

    full_result.to_excel(output_path, index=False, engine='xlsxwriter')      