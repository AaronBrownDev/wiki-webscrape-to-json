from bs4 import BeautifulSoup
import requests, json

# Lists to keep track of visited and upcoming pages
visited_pages = []
to_be_visited_pages = ["https://en.wikipedia.org/wiki/Spinal_stenosis", "https://en.wikipedia.org/wiki/Health_care", "https://en.wikipedia.org/wiki/Stenosis"]

def main(url: str):

    # *** 1. Fetch and Parse Wikipedia Page ***

    page = requests.get(url)  # Get the HTML content of the page
    soup = BeautifulSoup(page.text, "lxml")  # Parse the HTML for easier manipulation

    # Find the main content area of the Wikipedia page
    text_section = soup.find("div", class_="mw-content-ltr mw-parser-output")

    # Get all headers, paragraphs, and list items within the main content
    paragraphs = text_section.findAll(["h2", "h3", "p", "li"])
    
    # Get all the links within the main content
    hrefs = text_section.findAll(["a"])

    # *** 2. Initialize Data Storage and Variables ***

    wiki_content = {}  # Dictionary to hold the extracted content
    header = url[url.rfind('/') + 1:]  # Extract page title from URL 
    subheader = "Overview"  # Default subheader for initial content
    temp = 0  # Counter for tracking paragraph numbering within sections

    # *** 3. Depth-First Search for More Wikipedia Pages ***

    for href in hrefs:
        # Check if the link is a valid Wikipedia article (starts with "/wiki/", not a file, not a special category)
        if href.get("href", "INCORRECT")[:6] == "/wiki/" and href.get("href")[6:10] != "File" and href.get("href")[6:13] != "Special" and f"https://en.wikipedia.org{href.get('href')}" not in visited_pages:
            # Add the new page to the list of pages to be visited
            to_be_visited_pages.append(f"https://en.wikipedia.org{href.get('href')}")

    # *** 4. Extract and Structure Text Content ***

    for paragraph in paragraphs:

        # If it's a main header (h2), update the header and reset subheader
        if paragraph.name == "h2":
            header = paragraph.text[:paragraph.text.find("[")]  # Remove potential '[edit]' etc.
            subheader = "Overview"

        # If it's a subheader (h3), update the subheader
        elif paragraph.name == "h3":
            subheader = paragraph.text[:paragraph.text.find("[")]

        # If it's plain text, store it under the appropriate header and subheader
        else:
            # Initialize keys in the dictionary if they don't exist (avoids errors)
            if header not in wiki_content:
                wiki_content[header] = {}
            if subheader not in wiki_content[header]:
                wiki_content[header][subheader] = {}
                temp = 0  # Reset paragraph counter for new subheader

            if len(paragraph.text.rstrip("\n")) == 0: # Skip empty paragraphs
                continue

            # Ignore "References" and "External links" sections
            if "Reference" in header or "External link" in header:
                del wiki_content[header]
                continue

            # Add the paragraph text to the structured dictionary
            wiki_content[header][subheader][temp] = paragraph.text.rstrip("\n")
            temp += 1  # Increment paragraph counter

    # *** 5. Save Extracted Data as JSON ***

    with open(f"JSON-DATA/{url[url.rfind('/'):]}.json", "w") as outfile:
        json.dump(wiki_content, outfile)


# *** Main Program Execution ***

if __name__ == "__main__":

    while len(to_be_visited_pages) > 0:
        url = to_be_visited_pages.pop(0)  # Get the next page to visit
        visited_pages.append(url)        # Mark the page as visited
        main(url=url)  # Recursively scrape the new page