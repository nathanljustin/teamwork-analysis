class PythonController < ApplicationController
    def overallBar
        system 'python lib/overallDistribution.py'
        redirect_to '/overallBar/'
    end

    def importData
        path = params[:file].path
        full_call = 'python lib/importData.py ' + path
        if system (full_call)
            flash[:notice] = 'Import was successful.'
        else
            flash[:notice] = 'Import failed.'
        end
        redirect_to '/'
    end

    def deleteData
        if system 'python lib/delete_data.py'
            flash[:notice] = 'Deleted data successfully.'
        end
        redirect_to '/'
    end
end
