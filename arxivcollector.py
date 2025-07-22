# Inspired by: Fatima, R., Yasin, A., Liu, L., Wang, J., & Afzal, W. (2023). Retrieving arXiv, SocArXiv, and SSRN metadata for initial review screening. Information and Software Technology, 161, 107251. https://doi.org/10.1016/j.infsof.2023.107251

import httpx
from bs4 import BeautifulSoup
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import pandas as pd
import datetime
import urllib.parse
import sys
import argparse
import logging 

MAX_RETRIES = 3

class ArXivCollector():
    def __init__(self, 
                 user_agent="Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                 num_abstracts=50,
                 arxiv_doi_prefix="https://doi.org/10.48550",
                 default_item_type="ARTICLE",
                 verbose=False, 
                 mode="bibtex") -> None:
        self.user_agent = user_agent
        self.num_abstracts = num_abstracts
        self.arxiv_doi_prefix = arxiv_doi_prefix
        self.default_item_type = default_item_type
        self.verbose = verbose
        self.client = httpx.Client(headers={"User-Agent": self.user_agent,})
        self.title = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.mode = mode

        logging.basicConfig(level=logging.INFO,
                            force = True, handlers=[logging.StreamHandler(sys.stdout)])

        # Error handling for the mode parameter
        if self.mode not in ["bibtex", "csv"]:
            raise ValueError("The mode parameter must be either 'bibtex' or 'csv'.")

    def set_title(self, title: str):
        self.title = f"{title}"

    def send_request(self, url, method="GET"):
        for attempt in range(MAX_RETRIES):
            try:
                res = self.client.request(method, url, timeout=15)
                return res
            except httpx.RequestError as exc:
                logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
                if attempt < MAX_RETRIES - 1:  # i.e. not the last attempt
                    logging.info(f"Retrying... (Attempt {attempt + 2} of {MAX_RETRIES})")
                else:
                    logging.error(f"Failed to send request after {MAX_RETRIES} attempts.")
        return None
    
    def extract_text(self,soup:BeautifulSoup,selector):
        try:
            text = soup.select_one(selector).getText(strip=True)
        except AttributeError as err:
            text = None
        return text

    def find_data(self, soup: BeautifulSoup, keyword) -> str:
        sub, ann = None, None
        for p in soup.select('p'):
            if p.getText(strip=True).startswith(keyword):
                temp = p.getText(strip=True).split(';')
                sub = temp[0].strip().removeprefix('Submitted')
                ann = temp[-1].strip().removeprefix('originally announced')
                # Convert sub to a datetime object
                sub = datetime.datetime.strptime(sub, "%d %B, %Y")
                break
        return sub, ann
    
    def parse_html(self,response:httpx.Response):
        soup = BeautifulSoup(response.content,'html.parser')

        lis = soup.select('li.arxiv-result')
        if len(lis) == 0: return []
        for i,li in enumerate(lis,start=1):
            title =self.extract_text(li,'p.title')
            if self.verbose:
                print(i,title)
            
            temp_authors = li.select('p.authors>a')
            authors = ' AND '.join([', '.join(j.getText(strip=True).split()[::-1]) for j in temp_authors])

            Abstract = self.extract_text(li,'span.abstract-full').removesuffix('△ Less')

            extracted_text = self.extract_text(li,'p.comments > span:nth-of-type(2)')
            note = extracted_text if extracted_text else ""

            sub,ann = self.find_data(li,'Submitted')

            # Construct ID from first author's last name and year of submission
            id = authors.split(',')[0] + str(sub.year)

            link = li.select_one('p.list-title > a')['href']
            try:
                pdf = li.select_one('p.list-title > span > a[href*="pdf"]')['href']
            except TypeError:
                pdf = ""
            
            month_abbr = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

            yield { # BibTeX-friendly format
                "title":title,
                "author":authors,
                "abstract":Abstract,
                "note":note,
                "year":str(sub.year),
                "month": month_abbr[sub.month],
                "doi": f"{self.arxiv_doi_prefix}/arXiv.{link.split('/')[-1]}", # Construct the DOI from the arXiv ID
                "howpublished" : fr"\url{{{pdf}}}",
                "ENTRYTYPE": self.default_item_type,
                "ID": id
            }

    def run(self, url):
        self.mainLIST = []
        page = 0
        while True:
            # Parse the URL and its parameters
            parsed_url = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed_url.query)
            
            # Update the 'start' parameter
            params['start'] = [page*self.num_abstracts]
            
            # Construct the new URL
            new_query = urllib.parse.urlencode(params, doseq=True)
            if 'advanced' not in params:
                new_query = 'advanced=&' + new_query
            new_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
            res = self.send_request(new_url)
            results = list(self.parse_html(res))
            self.mainLIST.extend(results)
            logging.info(f"Scraped abstracts {page*self.num_abstracts} - {len(self.mainLIST)}")
            
            if self.mode == 'bibtex':
                # Create a BibDatabase
                db = BibDatabase()
                db.entries = self.mainLIST
                
                # Write the BibDatabase to a BibTeX file
                writer = BibTexWriter()
                with open(f'{self.title}.bib', 'w') as bibfile:
                    bibfile.write(writer.write(db))
            elif self.mode == 'csv':
                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(self.mainLIST)
                
                # Write the DataFrame to a CSV file
                df.to_csv(f'{self.title}.csv', index=False)

            page += 1
            if len(results) < self.num_abstracts: break

def main():
    parser = argparse.ArgumentParser(description='Retrieve arXiv metadata.')
    parser.add_argument('url', help='The URL to scrape.')
    parser.add_argument('title', help='The title for the output file.')
    args = parser.parse_args()

    arxiv = ArXivCollector()
    arxiv.set_title(args.title)
    arxiv.run(args.url)

if __name__ == '__main__':
    main()