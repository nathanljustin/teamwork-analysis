class CreateStudents < ActiveRecord::Migration[5.1]
  def change
    create_table :students do |t|
      t.integer :style
      t.string :name
      t.integer :team

      t.timestamps
    end
  end
end
