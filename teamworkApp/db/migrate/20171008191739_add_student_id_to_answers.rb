class AddStudentIdToAnswers < ActiveRecord::Migration[5.1]
  def change
    add_column :answers, :student_id, :integer
  end
end
