class PythonController < ApplicationController
    def evaluateAnswers
        require "rubypython"
        RubyPython.start
        # Might be good to have a graph object that we create for the ones that produce a graph. 
        
        # Not positive that this path will actually work. Rails is weird about where it likes its files to be. We may have to move the python files or find a new way to direct the path.
        fileName = RubyPython.import("/lib/evaluateAnswers.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
    end

    def generateData
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/generateData.py")
        p fileName.main(args).rubify
        RubyPython.stop
    end

    def generateTeams
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/generateTeams.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
    end

    def importData
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/importData.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec or execfile instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
    end

    def overallPie
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/overallPie.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
    end

    def studentGraph
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/studentGraph.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
    end
end
