# Dead Dove: Do Not Eat (/jk)

I wanted to know about the history of the _Dead Dove: Do Not Eat_ tag on the
AO3 so spun up this little program for getting some stats on tag usage over
time. It uses [this unofficial AO3 API](https://ao3-api.readthedocs.io/). It's
nothing too fancy, just the result of an evening falling down a little rabbit
hole.

## To run:

- Install `requirements.txt` using `pip install -r requirements.txt` or
  similar. This was written using `Python 3.8.10`.
- Run `python3 ao3-stats.py`.
- You will be prompted from the command line to enter the tag you're interested
  in analyzing. Copy and paste it _exactly_ from AO3 and press Enter.
- The script will generate a JSON file that (assuming nothing has gone wrong)
  includes all of the metadata, etc. for all of the fics from the tag you
  provided.
