# muddersOnRails()
# Sara McAllister November 17, 2017
# Last updated: 11-17-2017

# delete all data from database (this is super sketch)
import dbCalls

def main():
    print('Deleting everything from students, styles, and answers.')
    dbCalls.remove_all()

if __name__ == "__main__":
    main()


