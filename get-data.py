"""
Get work info from a list of IDs, 
provided as a command line argument.

Not linted. Sorry in advance.
"""

import AO3_fork as AO3
import json
import sys
import time
from math import ceil
from requests import exceptions
from tqdm import tqdm


def get_work(work_id, num_retries=60, wait_time=60):
    while num_retries > 0:
        try:
            work = AO3.Work(work_id)
            return work
        except (AO3.utils.HTTPError, 
                exceptions.Timeout,
                exceptions.TooManyRedirects,
                exceptions.RequestException) as e:
            print("Failed with error '{}' on work {}. ".format(e, work_id) +
                    "Waiting {} seconds ".format(wait_time) +
                    "({} retries remaining)...".format(num_retries))
            time.sleep(wait_time)
            num_retries -= 1
    print("Something is very wrong. Skipping this work; entire process may fail.")
    return


def get_work_info(work):
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
        return work_info


def main():

    work_ids = []
    in_filepath = sys.argv[1]
    with open(in_filepath, 'r') as input_file:
        for line in input_file.readlines():
            work_ids.append(line.rstrip('\n'))

    tag = in_filepath.split('_')[2]

    start_id = str(int(input(
        "(optional) What work ID do you want to begin on? " + 
        "(will re-collect all IDs after this one) ") or work_ids[0]))
    start_index = work_ids.index(start_id)

    date = time.strftime("%Y%m%d", time.gmtime())
    bad_filepath = "temp_{}_{}.json".format(tag, date)

    # This is kind of gross but pickling the AO3.Work objects didn't work
    # so this is what we're doing to allow restarting mid-collection:
    # Making a bad, incorrect JSON as the in-progress file
    # and then fixing it once everything is done. Sorry
    # but I didn't want to have to completely re-write the file every time
    if start_index == 0:
        with open(bad_filepath, 'w') as bad_file:
            first_work = get_work(work_ids[0])
            json.dump([get_work_info(first_work)], bad_file)
            bad_file.write('\n')

    print("\nProcessing {} fics (this may take some time) ...".format(
        len(work_ids)))
    for i in tqdm(range(start_index + 1, len(work_ids)),
            initial = start_index + 1,
            total = len(work_ids)):
        with open(bad_filepath, 'a') as stream:
            json.dump([get_work_info(get_work(work_ids[i]))], stream)
            stream.write('\n')
   
    # Yep so here's re-reading in the whole bad JSON
    # (just in case collection stopped and was restarted midway)
    all_work_info = []
    with open(bad_filepath, 'r') as stream:
        for line in stream.readlines():
            all_work_info.append(json.loads(line)[0])

    filename = "ao3_stats_{}_{}.json".format(tag, date)
    print("Saving results to '{}'...".format(filename))
    with open(filename, "w") as filepath:
        json.dump(all_work_info, filepath, indent = 4)
    print("Done!")
    print("")

    return


if __name__ == "__main__":
    main()
