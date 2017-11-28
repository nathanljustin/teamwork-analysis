class StudentGraphController < ApplicationController
    def show
        # @students: Stores all the student objects
        # @selected: Stores whether the student was selected previously or not
        # @image: Stores the image name of the graph (if available)

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

        # Check if summary graph has been created or not
        if File.exist?(Rails.root.join('app', 'assets', 'images', 'summary.png'))
            @image = 'summary.png'
        else
            @image = ''
        end
    end

    def graph
        if params[:selection].present?
            # Turn selected inputs into an array
            c = []
            for id in params[:selection][:selected]
                if id != ""
                    c.push(id)
                end
            end

            # Call the python function for the graph
            a = params[:selection][:selected].join(" ")        
            system 'python lib/studentGraph.py' + a
        end

        redirect_to student_graph_show_path(:id => c) 
    end
end
