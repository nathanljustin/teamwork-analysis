# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

students = Student.create([{name: 'Eloise Backer'}, {name: 'Ryan New'}, {name: 'Navier Leek'}])
Answer.create([
	{question: 1, student: students.first, value: 0},
	{question: 2, student: students.first, value: 0},
	{question: 3, student: students.first, value: 1},
	{question: 4, student: students.first, value: 2},
	{question: 5, student: students.first, value: 6},
	])