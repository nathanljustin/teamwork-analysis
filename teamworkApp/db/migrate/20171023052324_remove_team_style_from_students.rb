class RemoveTeamStyleFromStudents < ActiveRecord::Migration[5.1]
  def change
    remove_column :students, :style, :integer
    remove_column :students, :team, :integer
  end
end
