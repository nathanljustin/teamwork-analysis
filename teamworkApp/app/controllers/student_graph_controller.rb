class StudentGraphController < ApplicationController
    def show
        @selection = Selection.new
        @students = Student.all

        # Precheck boxes based on  what was previously checked
        id = (params[:id].present? ? params[:id] : [])
        temp = {}
        for student in @students
            idstr = student.id.to_s
            if id.include? idstr
                temp[idstr] = "checked"
            else
                temp[idstr] = ""
            end
        end
        @selected = temp
    end

    def graph
        # Turn selected inputs into an array
        c = []
        for id in params[:selection][:selected]
            if id != ""
                c.push(id)
            end
        end

        # Call the python function for the graph
        a = params[:selection][:selected].join("")        
        system 'python lib/studentGraph.py' + ' ' + a

        redirect_to student_graph_show_path(:id => c) 
    end
end
