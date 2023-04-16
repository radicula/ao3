"""
Get work info from a list of IDs, 
provided as a command line argument.

Not linted. Sorry in advance.
"""

import AO3_fork as AO3
import json
import sys
import time
import yaml
from math import ceil
from tqdm import tqdm


def get_work(work_id, num_retries=30, wait_time=30):
    while num_retries > 0:
        try:
            work = AO3.Work(work_id)
            return work
        except (AO3.utils.HTTPError, MaxRetryError) as e:
            print("Rate limit exceeded on work {}. ".format(work_id) +
                    "Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this work; entire process may fail.")
    return


def main():

    with open(sys.argv[1], 'r') as input_file:
        work_ids = json.load(input_file)

    print("\nProcessing {} fics (this may take some time) ...".format(len(work_ids)))
    works = []
    for work_id in tqdm(work_ids):
        works.append(get_work(work_id))

    works_info = []
    for work in works:
        work_info = {}
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
        works_info.append(work_info)

    date = time.strftime("%Y%m%d", time.gmtime())
    filename = "ao3_stats_{}_{}.json".format(
            ''.join(l for l in tag if l.isalnum()), date)
    print("Saving results to '{}'...".format(filename))
    with open(filename, "w") as filepath:
        json.dump(works_info, filepath, indent = 4)
    print("Done!")
    print("")

    return


if __name__ == "__main__":
    main()
