"""
Little program to scrape some basic information about a given AO3 tag.
Not fancy. A little more Comp Sci 101 than SWE.

2023 April 15

Not linted. Sorry in advance.
"""

import AO3
from math import ceil
from tqdm import tqdm


def tag_search(tag, page=1):
    search = AO3.Search(tags=tag)
    search.page = page
    search.update()
    return search


def print_results(search):
    # Just for debugging help
    print(search.total_results)
    for result in search.results:
        print(result)


def main():
    #tag = input("\nWhat tag would you like to investigate? ")
    #print("Investigating '{}'...".format(tag))
    tag = "Lucy Carlyle/George Cubbins | George Karim/Anthony Lockwood"
    tag = "Protective Quill Kipps"

    search = tag_search(tag)
    num_pages = ceil(float(search.total_results)/20.0)

    print("Processing {} pages of search results ...".format(num_pages))
    work_ids = []
    for page in tqdm(range(1, num_pages + 1)):
        s = tag_search(tag, page)
        work_ids = work_ids + [r.id for r in search.results]

    print("Processing {} fics (this may take some time) ...".format(len(work_ids)))
    works = []
    for work_id in tqdm(work_ids):
        works.append(AO3.Work(work_id))

    print("")

    #print(work.date_published)
    return


if __name__ == "__main__":
    main()
