class PythonController < ApplicationController
    def overallBar
        system 'python3 lib/overallDistribution.py'
        redirect_to '/overallBar/'
    end

    def importData
        path = params[:file].path
        # call the python command without printing error messages
        full_call = 'python3 lib/importData.py ' + path 
        if system full_call
            flash[:notice] = 'Import was successful.'
        else
            flash[:notice] = 'Import failed.'
        end
        redirect_to '/'
    end

    def deleteData
        if system 'python3 lib/delete_data.py'
            flash[:notice] = 'Deleted data successfully.'
        end
        redirect_to '/'
    end
end
