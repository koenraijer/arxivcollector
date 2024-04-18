arXivCollector
======

**arXivCollector** allows you to export your arXiv searches as neatly formatted BibTex files for easy importation in most common scientific reference managers (like Zotero or EndNote). It does not require much prior programming knowledge. A particularly useful feature is the inclusion of DOIs and direct links to article PDFs in the resulting file. The references can also be saved as a csv file.

Installation
------

1. Have Python installed (download it from [here](https://www.python.org/downloads/)).
2. Clone the repository by running the following command in a terminal:
```bash
git clone https://github.com/koenraijer/arxivcollector.git
```
3. Navigate to the cloned repository:
```bash
cd path/to/arxivcollector
```

Getting started
------

**arXivCollector** can be used in two ways:
- By importing the `arXivCollector()` class; 
- By executing the `arxivcollectory.py` script from the command line. 

### Step 1: obtain an arXiv search results URL 
To obtain an arXiv search results URL for your search query, go to [https://arxiv.org/](https://arxiv.org/) or to the [advanced search page](https://arxiv.org/search/advanced) and construct your search query. Press the big blue button that says "Search", wait until you arrive on the page that displays the search results. Now copy the entire URL as is, and you're done ✅. 

### Step 2: use arXivCollector in one of two ways
#### In Python
Run the following Python code (e.g., in a script or from a Jupyter notebook). 

```python
from arxiv import arXivCollector

# Initiate a new instance of the arXivCollector class
collector = arXivCollector()
# Set the title of the exported file (optional)
collector.set_title("Parrots")
# Pass the search URL to the run method
collector.run('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first')
```

After running this with your own search URL and title, a new file should appear in the parent directory of arXivCollector. 

#### From the commandline
The first argument after `arxivcollectory.py` is the search URL, the second argument is your title. 

```bash
python arxivcollector.py "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first" "Parrots"
```

API
------

### Class: arXivCollector

This class is used to collect metadata from the arXiv website and save it in either BibTeX or CSV format.

#### `__init__(self, user_agent, num_abstracts, arxiv_doi_prefix, default_item_type, verbose, mode) -> None`

Initializes an instance of the ArXiv class.

##### Parameters:

- `user_agent` (str): The User-Agent header to use when sending requests. Default is a common User-Agent string for a Chrome browser.
- `num_abstracts` (int): The number of abstracts you want displayed per page (on the arXiv website). Default is 50.
- `arxiv_doi_prefix` (str): The prefix for the DOI of arXiv papers. Default is "https://doi.org/10.48550".
- `default_item_type` (str): The default item type for the BibTeX entries. Default is "ARTICLE".
- `verbose` (bool): Whether to print verbose output. Default is False.
- `mode` (str): The mode to use when saving the collected data. Can be either "bibtex" or "csv". Default is "bibtex".

#### `set_title(self, title: str)`

Sets the title of the output file.

##### Parameters:

- `title` (str): The title to set.

#### `run(self, url)`

Starts the collection process for the specified URL.

##### Parameters:

- `url` (str): The URL to start the collection process for.