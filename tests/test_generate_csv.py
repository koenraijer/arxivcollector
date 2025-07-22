from pathlib import Path

from example import create


def test_create_csv():
    url = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=stochastic+parrot&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'
    create(url, "output", "csv")
    create(url, "output", "bibtex")

    # Check if file exists
    filenamecsv = "output.csv"
    filenamebib = "output.bib"
    assert Path(filenamecsv).exists(), "csv file was not created."
    assert Path(filenamebib).exists(), "bibtex file was not created."
