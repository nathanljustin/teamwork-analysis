class AddStylesToStudents < ActiveRecord::Migration[5.1]
  def change
    add_column :students, :communicator, :integer
    add_column :students, :collaborator, :integer
    add_column :students, :challenger, :integer
    add_column :students, :contributor, :integer
    add_column :students, :team_id, :integer
  end
end
