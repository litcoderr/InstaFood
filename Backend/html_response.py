import codecs
from bs4 import BeautifulSoup as bs

def generate(results):
    response = ""
    f=codecs.open("./static/response_template/card_template.html", 'r', 'utf-8')
    card_temp = bs(f.read(), 'html.parser')
    response += str(card_temp)
    
    # call --> str(response) || to get string from bs object
    return response

if __name__ == "__main__":
    generate("some results in dictionary")