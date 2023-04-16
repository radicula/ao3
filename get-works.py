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
from tqdm import tqdm


def tag_search(tag, page=1, num_retries=30, wait_time=30):
    while num_retries > 0:
        try:
            search = AO3.Search(tags=tag)
            search.page = page
            search.update()
            return search
        except (AO3.utils.HTTPError, MaxRetryError) as e:
            print("Rate limit exceeded on page {}. ".format(page) + 
                    "Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this page. Everything will probably break.")
    return 


def get_work_id(search_result, num_retries=30, wait_time=30):
    while num_retries > 0:
        try:
            work_id = search_result.id
            return work_id
        except (AO3.utils.HTTPError, MaxRetryError):
            print("Rate limit exceeded on work {}. ".format(page) + 
                    "Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
           time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this work; entire process may fail.")
    return


def main():

    tag = input("\nWhat tag would you like to investigate? " + 
            "(copy and paste it exactly!) ")
    print("Investigating '{}'...".format(tag))

    search = tag_search(tag)
    num_pages = ceil(float(search.total_results)/20.0)

    print("Processing {} pages of search results ...".format(num_pages))
    work_ids = []
    for page in tqdm(range(1, num_pages + 1)):
        s = tag_search(tag, page)
        for result in s.results:
            work_ids.append(get_work_id(result))

    date = time.strftime("%Y%m%d", time.gmtime())
    filename = "work_ids_{}_{}.json".format(
            ''.join(l for l in tag if l.isalnum()), date)
    print("Saving IDs to '{}'...".format(filename))
    with open(filename, "w") as filepath:
        json.dump(works_info, filepath)
    print("Done!")
    print("")

    return


if __name__ == "__main__":
    main()
