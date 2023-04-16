"""
Little program to scrape some basic information about a given AO3 tag.
Not fancy. A little more Comp Sci 101 than SWE.

2023 April 15

Not linted. Sorry in advance.
"""

import AO3
import tqdm

def main():
    tag = input("\nWhat tag would you like to investigate? ")
    print("Investigating '{}'...\n".format(tag))
    return

if __name__ == "__main__":
    main()
