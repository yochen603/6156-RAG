from idlelib import query

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def search_papers(query, api_key):
    # Abstract retrieval function
    def abstract_retrieval(urls):
        selectors = {
            'www.sciencedirect.com': "div.abstract.author div[id^='aep-abstract-sec']",
            'ieeexplore.ieee.org': "div[_ngcontent-c170] xplmathjax",
            'link.springer.com': "div.c-article-section__content",
            'dl.acm.org': "div.abstractSection.abstractInFull",
            'arxiv.org': "blockquote.abstract",
            'academic.oup.com': "section.abstract p.chapter-para",
            'www.aeaweb.org': "section.article-information.abstract",
            'iopscience.iop.org': "div.article-text.wd-jnl-art-abstract p",
        }

        abstracts = {}
        for url in urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            selector = selectors.get(domain)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            if selector:
                abstract_element = soup.select_one(selector)
                abstract_text = abstract_element.text.strip() if abstract_element else None
            else:
                abstract_text = None

            abstracts[url] = abstract_text

        return abstracts

    # Function to search Google Scholar and retrieve papers
    def search_google_scholar(query, api_key):
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": api_key
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        papers = []
        if 'organic_results' in results:
            for result in results['organic_results'][:10]:
                title = result['title']
                link = result['link']
                snippet = result.get('snippet', '')
                papers.append({
                    'title': title,
                    'link': link,
                    'abstract': snippet
                })

        # Try to fetch abstracts from the links
        urls = [paper['link'] for paper in papers]
        abstracts = abstract_retrieval(urls)

        # Update papers with abstracts
        for paper in papers:
            if abstracts.get(paper['link']):
                paper['abstract'] = abstracts[paper['link']]

        return papers

    # Call the search function
    print('retrieving papers.....')
    papers = search_google_scholar(query, api_key)

    return papers


if __name__ == '__main__':
    YOUR_API_KEY = "a3210d9144d16801c3abe0ead3c722df14fa68a26b7312a2a69dd098b484dbf4"
    query = 'img seg'
    print(search_papers(query, YOUR_API_KEY))










# Usage example
"""api_key = "a336033f0bdd0a1323caed9e65e0ab1e1d3fd07254a5164b16f6a5ed7b3792f2"
query = "transformer original paper"
papers = search_papers(query, api_key)

for paper in papers:
    print(f"Title: {paper['title']}\nLink: {paper['link']}\nAbstract: {paper['abstract']}\n")
print(papers)"""

'''
def extract_abstract(url):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    response = requests.get("url", headers=headers)
    html_content = response.text

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.prettify())

def search_paper(params):
    paper_info=[]
    search = serpapi.search(params)
    results = search.as_dict()
    organic_results = results["organic_results"]
    for result in organic_results:
        paper_dict = {
            "title": result.get("title", ""),
            "link": result.get("link", ""),
        }
        paper_info.append(paper_dict)
    return paper_info
'''