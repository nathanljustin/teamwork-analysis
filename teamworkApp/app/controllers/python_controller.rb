class PythonController < ApplicationController
    def overallBar
        system 'python lib/overallBar.py'
        redirect_to '/overallBar/'
    end

    def studentGraph
        system 'python lib/studentGraph.py 1'
        redirect_to '/studentGraph/'
    end

    def importData
        path = params[:file]
        system 'python lib/importData.py test/test_spreadsheet.csv'
        redirect_to '/'
    end
end
