ArXiv Metadata Collector
======

ArXiv Metadata Collector is a simple script that allows you to transform your arXiv searches into neatly formatted BibTex files for easy importation in most common scientific reference managers (like Zotero or EndNote). It does not require much prior programming knowledge. A particularly useful feature is the inclusion of DOIs and direct links to article PDFs in the resulting file. The references can also be saved as a csv file.

Installation
------

1. Make sure to have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. Clone the repository. Open your terminal and run the following command:
```bash
git clone https://github.com/your_username/your_repository.git
```
3. Navigate into the cloned repository:
```bash
cd path/to/your_repository
```

Getting started
------

You can use **arXivCollector** in two ways:
- By importing the class
- By using the script on the commandline. 

### Obtaining the URL 
To obtain the right URL for your search query, simply go to [https://arxiv.org/](https://arxiv.org/) or to the [advanced search page](https://arxiv.org/search/advanced) and construct your search query. Press the big blue button that says "Search", wait until you arrive at the results page, and copy the entire URL. 

### In Python
```python
from arxiv import arXivCollector

collector = arXivCollector()
collector.set_title("Parrots")
collector.run('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first')
```

### From the commandline
```bash
python arxivcollector.py "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first" "Parrots"
```

API
------

### Class: arXivCollector

This class is used to scrape metadata from the arXiv website and save it in either BibTeX or CSV format.

#### `__init__(self, user_agent, num_abstracts, arxiv_doi_prefix, default_item_type, verbose, mode) -> None`

Initializes an instance of the ArXiv class.

##### Parameters:

- `user_agent` (str): The User-Agent header to use when sending requests. Default is a common User-Agent string for a Chrome browser.
- `num_abstracts` (int): The number of abstracts to scrape per page. Default is 50.
- `arxiv_doi_prefix` (str): The prefix for the DOI of arXiv papers. Default is "https://doi.org/10.48550".
- `default_item_type` (str): The default item type for the BibTeX entries. Default is "ARTICLE".
- `verbose` (bool): Whether to print verbose output. Default is False.
- `mode` (str): The mode to use when saving the scraped data. Can be either "bibtex" or "csv". Default is "bibtex".

#### `set_title(self, title: str)`

Sets the title of the output file.

##### Parameters:

- `title` (str): The title to set.

#### `run(self, url)`

Starts the scraping process for the specified URL.

##### Parameters:

- `url` (str): The URL to start the scraping process for.