import pandas as pd

from read_website import *

from create_final_output import *

def get_keywords():

    keywords = []
    with open('keywords.txt') as file:
        keywords.extend(file.readlines())

    keywords = [word.replace('\n', '').strip() for word in keywords]

    return keywords

def get_contextual_words():

    contextual_words = set()
    with open('Contextual Words.txt') as file:
        contextual_words.update(file.readlines())

    contextual_words = [word.replace('\n', '') for word in contextual_words]

    return contextual_words

if __name__ == "__main__":

    company_name = "Output Files/290_Repsol.xlsx"

    df = pd.read_excel(company_name)
    
    result = get_text(df, get_keywords())

    result.to_excel("Output1.xlsx", index=False, engine='xlsxwriter')

    ans = input("Ready for contextual part\t:")

    if ans == 'yes':

        save_final_output(company_name)