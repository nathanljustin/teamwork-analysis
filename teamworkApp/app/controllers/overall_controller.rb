class OverallController < ApplicationController
    def show
        # @image: Stores the image name of the graph (if available)
        graph

        # Check if overall graph has been created or not
        if File.exist?(Rails.root.join('app', 'assets', 'images', 'overall.png'))
            @image = 'overall.png'
        else
            graph
        end
    end

    def graph
        system 'python lib/overallDistribution.py'
    end
end
