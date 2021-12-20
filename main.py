"""
Improving 한국어 vocabulary using a Python script
This script followed the project of Niamh Kingsley entitled "How I Used Python Code to Improve My Korean". Changes were
made along the way as there were errors encountered upon running the script (e.g., AttributeError, translation not working
for googletrans)
Link to Kingsley's Project: https://towardsdatascience.com/how-i-used-python-code-to-improve-my-korean-2f3ae09a9773?gi=68193ec584c4

Jan Luis Antoc
"""
# Solved issue with SystemError: java.nio.file.InvalidPathException by following the recommendation on the link below -
# https://stackoverflow.com/questions/65842567/systemerror-java-nio-file-invalidpathexception
from konlpy.tag import Okt
from googletrans import Translator
from pandas import DataFrame


def translate(text):
    # There are four more POS tagging under KONLPy - Hannanum, Kkma, Komoran, and Mecab
    # Okt has a low loading and execution time
    okt = Okt()

    # Use pos() function of okt to make a dataframe
    trans = (okt.pos(text, norm=True, stem=True, join=True))
    korean_list = DataFrame(trans, columns=['Korean'])

    # Eliminating the punctuations was changed because of AttributeError: 'DataFrame' object has no attribute 'Type'
    korean_list = korean_list[korean_list['Korean'].str.contains("/Punctuation") == False]

    # Changed keep to first to retain the first occurrence of duplicates
    korean_list.drop_duplicates(keep="first", inplace=True)

    # Separate the Korean word from its type
    korean_list[['Korean', 'Type']] = korean_list['Korean'].str.split('/', expand=True)
    korean_list = korean_list.sort_values(by="Type")

    # Set up the translator
    translator = Translator()

    # Translate by adding a column
    # Error: AttributeError: 'NoneType' object has no attribute 'group'
    # Solution: Installing a specific version of googletrans -
    # https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group

    # Error: Translation not working, the Korean words are being retained in the English column
    # Cause of Error: This googletrans does not work at all times
    # Solution: Install a specific googletrans version (pip install googletrans==4.0.0rc1)
    # https://stackoverflow.com/questions/63077115/googletrans-python-not-translating
    korean_list['English'] = korean_list['Korean'].apply(translator.translate).apply(getattr, args=('text',))

    # Save in an html file
    # Edit the HTML file and make sure it has a meta charset of "UTF-8" so it will support 한국어
    # Change this based on your desired file name
    korean_list.to_html('KoreanParagraph.html')


if __name__ == '__main__':
    # Sometimes, an http error might be encountered. Just re-run the script
    sample = "내가 뭐랬어 이길 거랬잖아 믿지 못했어 (정말) 이길 수 있을까 이 기적 아닌 기적을 우리가 만든 걸까 (No) 난 여기 있었고 니가 내게 다가와준 거야"
    translate(sample)
