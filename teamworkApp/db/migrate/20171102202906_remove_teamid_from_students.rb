class RemoveTeamidFromStudents < ActiveRecord::Migration[5.1]
  def change
    remove_column :students, :team_id, :integer
  end
end
