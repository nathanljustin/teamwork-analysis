class PythonController < ApplicationController
<<<<<<< HEAD
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

    def overallPie
        require "rubypython"
        RubyPython.start
        sys = RubyPython.import("sys")
        sys.path.append('./lib')
        overallPie = RubyPython.import("overallPie.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        RubyPython.stop
    end

    def studentGraph
        require "rubypython"
        RubyPython.start
        fileName = RubyPython.import("/lib/studentGraph.py")
        # TODO: I don't know how is best to run all of these methods. perhaps use an exec instead of a main? that was we can run the whole file? 
        p fileName.main(args).rubify
        RubyPython.stop
=======
    def overallBar
        system 'python lib/overallBar.py'
        redirect_to '/overallBar/'
    end

    def studentGraph
        system 'python lib/studentGraph.py 1'
        redirect_to '/studentGraph/'
>>>>>>> 8eb5a02c5f819de06edcac64304b2844cc0e8830
    end
end
