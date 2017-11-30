class CreateCourses < ActiveRecord::Migration[5.1]
  def change
    create_table :courses do |t|
      t.string :name
      t.integer :year
      t.integer :semester
      t.integer :section
      t.string :course_code

      t.timestamps
    end
  end
end
