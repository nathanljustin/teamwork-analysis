class AddQuestionToAnswers < ActiveRecord::Migration[5.1]
  def change
    add_column :answers, :question, :integer
  end
end
