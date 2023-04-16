"""
Generates a file with the work IDs for all works in a given tag
-- Also allows for restarting midway through

Not linted. Sorry in advance.
"""

import AO3_fork as AO3
import json
import time
import yaml
from math import ceil
from requests import exceptions
from tqdm import tqdm


def tag_search(tag, page=1, num_retries=30, wait_time=60):
    while num_retries > 0:
        try:
            search = AO3.Search(tags=tag)
            search.page = page
            search.update()
            return search
        except (AO3.utils.HTTPError, 
                exceptions.Timeout,
                exceptions.TooManyRedirects,
                exceptions.RequestException) as e:
            print("Failed with error '{}' on page {}. ".format(e, page) + 
                    "Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this page. Everything will probably break.")
    return 


def main():

    tag = input("\nWhat tag would you like to investigate? " + 
            "(copy and paste it exactly!) ")
    start_page = int(input(
        "(optional) What page of results do you want to start on? ") or 1)
    print("Investigating '{}'...".format(tag))

    search = tag_search(tag, page=start_page)
    num_pages = ceil(float(search.total_results)/20.0)
    date = time.strftime("%Y%m%d", time.gmtime())
    filename = "work_ids_{}_{}.txt".format(
            ''.join(l for l in tag if l.isalnum()), date)

    if start_page == 1:
        with open(filename, 'w') as stream:
            for work in search.results:
                stream.write("{}\n".format(work.id))
        start_page = 2

    print("Processing {} pages of search results ...".format(num_pages))
    work_ids = []
    for page in tqdm(range(start_page, num_pages + 1)):
        s = tag_search(tag, page)
        with open(filename, 'a') as stream:
            for result in s.results:
                stream.write("{}\n".format(result.id))

    print("Done!")
    print("")

    return


if __name__ == "__main__":
    main()
