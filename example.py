from arxivcollector import ArXivCollector


def create(url, title="output", mode='bibtex'):
    # Initiate a new instance of the arXivCollector class
    collector = ArXivCollector()
    # Set the title of the exported file (optional)
    collector.set_title(title)
    collector.set_mode(mode)
    # Pass the search URL to the run method
    collector.run(url)


url = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'

create(url, "output", "csv")
