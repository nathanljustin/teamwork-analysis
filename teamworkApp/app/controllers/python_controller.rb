class PythonController < ApplicationController
    def overallBar
        system 'python lib/overallBar.py'
        redirect_to '/overallBar/'
    end

    def studentGraph
        @students = params[:students]
        puts @students
        system 'python lib/studentGraph.py 1'
        redirect_to '/python/studentGraph/'
    end
end
