class CreateAssignments < ActiveRecord::Migration[5.1]
  def change
    create_table :assignments do |t|
      t.integer :student_id
      t.integer :team_id

      t.timestamps
    end
  end
end
