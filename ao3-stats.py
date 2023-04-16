"""
Little program to scrape some basic information about a given AO3 tag.
Not fancy. A little more Comp Sci 101 than SWE.

2023 April 15

Not linted. Sorry in advance.
"""

import AO3_fork as AO3
import json
import time
import yaml
from math import ceil
from tqdm import tqdm


def tag_search(tag, page=1, num_retries=30, wait_time=15):
    while num_retries > 0:
        try:
            search = AO3.Search(tags=tag)
            search.page = page
            search.update()
            return search
        except AO3.utils.HTTPError:
            print("Rate limit exceeded. Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this page. Everything will probably break.")
    return 



def print_results(search):
    # Just for debugging help
    print(search.total_results)
    for result in search.results:
        print(result)


def get_work_id(search_result, num_retries=30, wait_time=15):
    while num_retries > 0:
        try:
            work_id = search_result.id
            return work_id
        except AO3.utils.HTTPError:
            print("Rate limit exceeded. Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this work; entire process may fail.")
    return


def get_work(work_id, num_retries=30, wait_time=15):
    while num_retries > 0:
        try:
            work = AO3.Work(work_id)
            return work
        except AO3.utils.HTTPError:
            print("Rate limit exceeded. Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
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

    print("Processing {} fics (this may take some time) ...".format(len(work_ids)))
    works = []
    for work_id in tqdm(work_ids):
        works.append(get_work(work_id))

    work_info = {}
    for work in works:
        work_info['id'] = work.id
        work_info['bookmarks'] = work.bookmarks
        work_info['categories'] = work.categories
        work_info['nchapters'] = work.nchapters
        work_info['characters'] = work.characters
        work_info['complete'] = work.complete
        work_info['comments'] = work.comments
        work_info['expected_chapters'] = work.expected_chapters
        work_info['fandoms'] = work.fandoms
        work_info['hits'] = work.hits
        work_info['kudos'] = work.kudos
        work_info['language'] = work.language
        work_info['rating'] = work.rating
        work_info['relationships'] = work.relationships
        work_info['restricted'] = work.restricted
        work_info['status'] = work.status
        work_info['summary'] = work.summary
        work_info['tags'] = work.summary
        work_info['title'] = work.title
        work_info['warnings'] = work.warnings
        work_info['words'] = work.words
        work_info['collections'] = work.collections
        work_info['date_edited'] = str(work.date_edited)
        work_info['date_published'] = str(work.date_published)
        work_info['date_updated'] = str(work.date_updated)

    date = time.strftime("%Y%m%d", time.gmtime())
    filename = "ao3_stats_{}_{}.json".format(
            ''.join(l for l in tag if l.isalnum()), date)
    print("Saving results to '{}'...".format(filename))
    with open(filename, "w") as filepath:
        json.dump(work_info, filepath, indent = 4)
    print("Done!")
    print("")

    return


if __name__ == "__main__":
    main()
