class PythonController < ApplicationController

    def evaluateAnswers
        require "rubypython"
        RubyPython.start
        sys = RubyPython.import(sys)
        sys.path.append('#{Rails.root}/lib')
        #There is something up here with the packages within evaluate answers (do we need to have all of python within our rails package cause uhh ...?)
        enum = RubyPython.import(enum)
        evalAnswers = RubyPython.import("evaluateAnswers")
        # Not positive that this path will actually work. Rails is weird about where it likes its files to be. We may have to move the python files or find a new way to direct the path.
        #fileName = RubyPython.import("/lib/evaluateAnswers.py")
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

    def overallBar
        require "rubypython"
        RubyPython.start
        sys = RubyPython.import("sys")
        sys.path.append('./lib')
        overallBar = RubyPython.import("overallBar")
        logger.debug overallBar.main()
        RubyPython.stop
        redirect_to '/overallBar/'
    end

    def studentGraph
        require "rubypython"
        RubyPython.start
        sys = RubyPython.import("sys")
        sys.path.append('./lib')
        studentGraph = RubyPython.import("studentGraph")
        logger.debug studentGraph.student_graph(1)
        RubyPython.stop
        redirect_to '/studentGraph/'
    end
end
