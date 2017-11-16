class StudentGraphController < ApplicationController
    def show
        @students = Student.all
    end
end
