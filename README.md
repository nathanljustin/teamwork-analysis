# teamwork-analysis

## Contents

* [Summary](#summary)
* [Contributors](#contributors)
* [Background Research Findings](#background-research-findings)
* [MVP Objectives](#mvp-objectives)
* [Functionality](#functionality)
* [Architecture](#architecture)
* [Past Issues](#past-issues)
* [Known Bugs](#known-bugs)
* [References](#references)

## Summary

Our project consists of two main parts, conducted in conjunction. The first part of our project was data visualization and teamwork research. We used Glenn Parker’s teamwork survey as our basis and obtained our data from student responses to the survey throughout the semester. With this, we developed a web interface that presents this data in graphical format and allows users to import data about their courses and teams. To enable this, we needed a few things: a database, amethod for the user to upload to the database, and a way to construct graphsfrom this data. The second part of our project consists of researching teamdynamics. We researched many different teamwork strategiesto estimate what consists of a good team.  When we fine tuned how we visualized the data CS 121 survey, we compiled the data and our researchto to produce graphs which show team dynamics.

## Contributers

* Nathan Justin 
* Sara McAllister
* Maeve Murphy
* Reagan Smith

## Problem Description

How can we use data collected from Glenn Parker’s Teamwork Survey and research into team dynamics to visualize details of team members and students, and create different types of well-structured teams to foster good work environments?

## Background Research Findings

From the research linked in the references section, the best teams are those with communicators, challengers, contributors, and collaborators represented. In particular, teams need a lot of communication to work well together so not having a strong communicator is a drawback to the team. Also, one challenger on a team is important, but more can cause problems.

## MVP objective

For our minimum viable product (MVP), we expect to deliver two main functionalities: a method to import survey data and a basic graphical representation of the data. To import survey data, we plan on allowing the user to enter a json with multiple people’s results from the survey. This data will then be stored in our database. The second part of our MVP is graphical interpretations of the data. For the MVP, we plan on visualizing the overall results of the data so that the user can see the proportions of challenger to communicator to collaborator to contributor for the class. We also plan to have a set of graphs that show a person’s individual scores and a set of graphs that will show the distribution of responses to each question. 

## Functionality

* The user can upload a CSV and the information will be saved to the database.
* The user can look at the overall distribution of the data between the four types.
* The user can select as many students as they want from the imported data and see the distribution of the selected students over the categories.
* When the user wants to look at a different set of students such as a different course, the user can delete the current information stored in the database and start the process over again.

## Architecture

The data processing will be done with Python using numpy. The processor will access the database which will be implemented in SQLite while we discuss data privacy concerns. Ruby will use the Python scripts to display the resulting graphs on a web page a user can access and add data too.
There will be a simple database to hold JSON strings, some Python scripts that access the data to build graphs using numpy, and a Ruby page to display these graphs when asked for. Initially, there will only be one graph that Python needs to construct and Ruby needs to display.

## Past Issues

None.

## Known Bugs

Currently does not work.

## References

### Teamwork Research

* Briggs,  Margaret  H. 1993. [Team Talk: Communication Skills for Early Intervention Teams.](http://journals.sagepub.com/doi/abs/10.1177/152574019301500106)
* Kirnan, Jean Powell; Diane Woodruff. 1994. [Reliability and Validity Estimates of the Parker Team Player Survey.](http://journals.sagepub.com/doi/abs/10.1177/0013164494054004020)
* Luca, Joe; Pina Tarricone. 2002. [Successful Teamwork: A CaseStudy.](http://www.unice.fr/crookall-cours/teams/docs/team%20Successful%20teamwork.pdf)
* Parker, Glenn M. 2008. Team Players and Teamwork New Strategies for Develop-ing Successful Collaboration. Jossey-Bass: San Francisco.

### Database Setup

* https://stackoverflow.com/questions/2098131/rails-how-to-list-database-tables-objects-using-the-rails-console
* https://www.justinweiss.com/articles/creating-easy-readable-attributes-with-activerecord-enums/
* http://www.tomjewett.com/dbdesign/dbdesign.php?page=manymany.php
* http://guides.rubyonrails.org/v3.2.8/migrations.html


### Python Scripts

* https://docs.python.org/3.6/library/sqlite3.html
* https://pythonspot.com/en/matplotlib-bar-chart/
* https://docs.python.org/3/library/contextlib.html
* https://docs.python.org/3.6/library/unittest.html


### UI

* https://startbootstrap.com/template-overviews/bare/
* https://github.com/twbs/bootstrap-sass
* https://github.com/thoughtbot/high_voltage

### Github

* https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

### Python Integration

* https://github.com/halostatue/rubypython
* https://mixandgo.com/blog/how-to-use-link_to-in-rails
* http://effbot.org/pyfaq/how-do-i-create-a-pyc-file.htm
* https://www.codesd.com/item/using-the-rubypython-gem-in-ruby-on-rails-how-do-you-call-a-python-script-from-the-lib-folder.html
* http://www.rubydoc.info/gems/rubypython/0.5.1/RubyPython
* https://github.com/halostatue/rubypython/issues/14

### Ruby on Rails

* https://www.tutorialspoint.com/ruby-on-rails/rails-controllers.htm
* http://guides.rubyonrails.org/action_controller_overview.html#methods-and-actions
* http://www.mattmorgante.com/technology/csv
* http://guides.rubyonrails.org/routing.html
* http://guides.rubyonrails.org/form_helpers.html#uploading-files