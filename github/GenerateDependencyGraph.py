#!/bin/env python

import GithubObjects

def generateGraph():
    classes = [ getattr( GithubObjects, c ) for c in dir( GithubObjects ) if hasattr( getattr( GithubObjects, c ), "_autoDocument" ) ]
    graph = "digraph D {\n"
    for c in classes:
        graph += c._dependencyGraph()
    graph += "}\n"
    return graph

if __name__ == "__main__":
    print generateGraph()
