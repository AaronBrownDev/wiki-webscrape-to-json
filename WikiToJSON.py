from bs4 import BeautifulSoup
import requests, json

def main(url : str):

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "lxml") # pip3 install lxml

    text_section = soup.find("div", class_ = "mw-content-ltr mw-parser-output")

    paragraphs = text_section.findAll(["h2", "h3", "p"])

    wiki_content = {}
    header = "Introduction"
    subheader = "Introduction"
    temp = 0    

    for paragraph in paragraphs:
        
        # When the paragraph is the header
        if paragraph.name == "h2":
            header = paragraph.text[:paragraph.text.find("[")] # wiki has a tendency to return text with brackets like [edit] at the end of headers
            subheader = "Introduction"
            
        # When the paragraph is the subheader
        elif paragraph.name == "h3":
            subheader = paragraph.text[:paragraph.text.find("[")]
        
        # When the paragraph is just plain text
        else:
            if header not in wiki_content:
                wiki_content[header] = {}
                wiki_content[header][subheader] = {}
                temp = 0
            elif subheader not in wiki_content:
                wiki_content[header][subheader] = {}
                temp = 0
            
            wiki_content[header][subheader][temp] = paragraph.text.rstrip("\n")
            temp += 1
            
        
    with open(f"JSON-DATA/{url[url.rfind('/'):]}.json", "w") as outfile: 
        json.dump(wiki_content, outfile)
    
    
if __name__ == "__main__":
    
    url = "https://en.wikipedia.org/wiki/Health_care"
    
    main(url = url)