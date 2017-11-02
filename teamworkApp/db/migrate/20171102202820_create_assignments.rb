class CreateAssignments < ActiveRecord::Migration[5.1]
  def change
    create_table :assignments do |t|
      t.string :student_id
      t.string :integer
      t.integer :team_id

      t.timestamps
    end
  end
end
