# muddersOnRails()
# Sara McAllister November 17, 2017
# Last updated: 11-17-2017

# delete all data from database and remove generated graphs (this is super sketch)

import os

import dbCalls

summary_file = 'app/assets/images/summary.png'
overall_file = 'app/assets/images/overall.png'

def main():
    dbCalls.remove_all()

    # remove both summary and overall picture
    try:
        os.remove(summary_file)
        os.remove(overall_file)
    except OSError:
        pass

if __name__ == "__main__":
    main()


