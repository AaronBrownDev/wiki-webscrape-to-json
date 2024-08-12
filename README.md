# WikiScraper for Stenosis Chatbot Training (Discontinued)

This Python script was part of a side project aimed at extracting structured text content from Wikipedia articles related to Stenosis and Spinal Stenosis.

 The intention was to convert this information into JSON format, which could then be used for training a chatbot designed to help people learn about these conditions.
Features

    Web Scraping: Utilized requests and BeautifulSoup to fetch and parse HTML content from Wikipedia pages.
    Depth-First Search: Implemented a depth-first search algorithm to explore linked pages, expanding the knowledge base.
    Data Structuring: Organized extracted content into a hierarchical dictionary with headers, subheaders, and numbered paragraphs.
    JSON Output: Saved the structured data in JSON files for easy integration with chatbot training frameworks.
    Target Focus: Specifically targeted pages related to Stenosis and health-related topics to ensure relevant information was gathered.