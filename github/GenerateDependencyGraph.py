import sys

import GithubObjects

class GraphGenerator:
    def __init__( self ):
        classes = [ getattr( GithubObjects, c ) for c in dir( GithubObjects ) if hasattr( getattr( GithubObjects, c ), "_autoDocument" ) ]

        self.dependencies = dict()
        self.dependents = dict()
        for c in classes:
            self.dependencies[ c.__name__ ] = set()
            self.dependents[ c.__name__ ] = set()
        for c in classes:
            for dependency in c._dependencies():
                self.dependencies[ c.__name__ ].add( dependency )
                self.dependents[ dependency ].add( c.__name__ )

    def execute( self ):
        self.reduceGraph()
        return self.generateString()

    def reduceGraph( self ):
        goOn = True
        while goOn:
            goOn = False
            for challengedClass in self.dependencies:
                if (
                    len( self.dependencies[ challengedClass ] ) == 0 # Sinks
                    or
                    len( self.dependents[ challengedClass ] ) == 0 # Sources
                    or
                    len( self.dependencies[ challengedClass ] ) == 1 and len( self.dependents[ challengedClass ] ) == 1 # Pass-through
                ):
                    self.removeClass( challengedClass )
                    goOn = True
                    break
        # self.removeClass( "Hook" )
        # self.removeClass( "Download" )
        # self.removeClass( "GitBlob" )
        # self.removeClass( "GitTag" )
        # self.removeClass( "GitRef" )
        # self.removeClass( "Branch" )
        # self.removeClass( "UserKey" )
        # self.removeClass( "Authorization" )
        # self.removeClass( "GistComment" )
        # self.removeClass( "GitTree" )
        # self.removeClass( "Label" )
        # self.removeClass( "RepositoryKey" )
        # self.removeClass( "Tag" )
        # self.removeClass( "GitCommit" )
        # self.removeClass( "PullRequestFile" )
        # self.removeClass( "AuthenticatedUser" )
        # self.removeClass( "IssueComment" )
        # self.removeClass( "PullRequestComment" )

    def removeClass( self, classToRemove ):
        for dependency in self.dependencies[ classToRemove ]:
            for dependent in self.dependents[ classToRemove ]:
                sys.stderr.write( dependent + " -> " + dependency  + " (through " + classToRemove + ")\n" )
                self.dependencies[ dependency ].add( dependent )
                self.dependents[ dependent ].add( dependency )
        for dependency in self.dependencies[ classToRemove ]:
            self.dependents[ dependency ].remove( classToRemove )
        for dependent in self.dependents[ classToRemove ]:
            self.dependencies[ dependent ].remove( classToRemove )
        del self.dependencies[ classToRemove ]
        del self.dependents[ classToRemove ]

    def generateString( self ):
        graph = "digraph D {\n"
        graph += "    node [shape=\"box\"];\n"
        for c in self.dependencies:
            for dependency in self.dependencies[ c ]:
                # if dependency not in [ "NamedUser", "Repository", "Organization" ]:
                    graph += "    " + c + " -> " + dependency + ";\n"
        graph += "}\n"

        return graph

if __name__ == "__main__":
    print GraphGenerator().execute()
