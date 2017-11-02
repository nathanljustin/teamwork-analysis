class CreateStyles < ActiveRecord::Migration[5.1]
  def change
    create_table :styles do |t|
      t.integer :student_id
      t.integer :communicator
      t.integer :collaborator
      t.integer :challenger
      t.integer :contributor

      t.timestamps
    end
  end
end
