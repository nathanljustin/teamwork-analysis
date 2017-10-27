class RemoveStylesFromStudents < ActiveRecord::Migration[5.1]
  def change
    remove_column :students, :communicator, :integer
    remove_column :students, :collaborator, :integer
    remove_column :students, :challenger, :integer
    remove_column :students, :contributor, :integer
  end
end
