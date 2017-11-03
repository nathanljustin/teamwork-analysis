class AddCourseIdToTeams < ActiveRecord::Migration[5.1]
  def change
    add_column :teams, :course_id, :integer
  end
end
