class StudentGraphController < ApplicationController
    def show
        @selection = Selection.new
        @students = Student.all
    end
    def graph
        a = params[:selection][:selected].join("")
        system 'python lib/studentGraph.py' + ' ' + a
        redirect_to '/student_graph/show'
    end
end
