# muddersOnRails()
# Sara McAllister November 8, 2017
# Last updated: 11-11-2017

# unittests for dbCalls.py and importData.py
# currently assumes an empty, created test database

# initialize db/test.sqlite3 by running 
# $ rails db:migrate RAILS_ENV=test 
# if the database is created but not empty, first run
# $ rails db:drop RAILS_ENV=test

# once db/test.sqlite3 is initialized perform tests by running
# $ python lib/tests.py -v
# the v flag is for a verbose output and not generally needed
# this code assumes python 3 and has not been tested on earlier python versions

import unittest

import importData
import overallBar
import studentGraph
import dbCalls

class TestDBCallsCase(unittest.TestCase):

    def setUp(self):
        importData.check_inputs('test/test_spreadsheet(1).csv', test=True)

    def test_import_data(self):
        # query for all inserted data
        students = dbCalls.get_all_students(test=True)
        student_ids = [student[0] for student in students]
        styles = dbCalls.get_students_styles(student_ids, test=True)
        answers = dbCalls.get_student_answers(student_ids[0], test=True)

        # check correct number of students
        self.assertEqual(3, len(students))        
        # check that student names are correct
        self.assertEqual(sorted([student[1] for student in students]), sorted(['jdoe','mcmurphy','rsmith']))
        # check that styles are correct
        self.assertEqual(sorted([style[5] for style in styles]), sorted([49, 49, 50]))
        self.assertEqual(sorted([style[3] for style in styles]), sorted([43, 43, 43]))
        self.assertEqual(sorted([style[2] for style in styles]), sorted([43, 48, 43]))
        self.assertEqual(sorted([style[4] for style in styles]), sorted([45, 39, 45]))

        self.assertEqual(18, len(answers))
      

    def tearDown(self):
        with dbCalls.dbconnect(True) as c:
            print('Clearing out test database')
            dbCalls.remove_all(test=True)


if __name__ == '__main__':
    unittest.main()