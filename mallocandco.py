#!/usr/bin/env python3

from octopus.server.DBInterface import DBInterface

projectName = 'android.tar.gz'
query = "queryNodeIndex('type:Function').id"

db = DBInterface()
db.connectToDatabase(projectName)

ids = db.runGremlinQuery(query)

CHUNK_SIZE = 256
LOCATION = '/home/sid/RABBIT_HOLE/CODE_ANALYSIS/joern/projects/octopus/data/projects/'
for chunk in db.chunks(ids, CHUNK_SIZE):

    query = """
        getCallsToRegex(".*read(Int|Uint)(32|64)")
        .statements()
        .out("REACHES")
        .has("code",textRegex(".*(malloc|memcpy).*"))
        .functions()
        .functionToLocationStr()
    """

    query2 = """
       getNodesWithTypeAndName(TYPE_FUNCTION, '*onTransact*')
       .out(FUNCTION_TO_AST_EDGE)
       .getArguments('(memcpy OR malloc)', '2')
       .out(USES_EDGE)
       .filter{
           it.get().value('code') == 'len'
       }
       .filter{
            it.in('USES')
            .filter{it.type == 'Condition'}.toList() == []
        }
       .functions()
       .functionToLocationStr()

    """

    query3 = """
    getCallsToRegex("getIntField").statements().out("REACHES")
    .has('code', textRegex('^((?!ALOG).)*$'))
    .has('code', textRegex('^((?!getIntField).)*$'))
    .has('type', 'Condition')
    .map{ it.get().value('code') }.pp()
    """
    query4 = """
getCallsToRegex(".*(g|G)etIntField.*")
.statements().out("REACHES")
.has('code',textRegex('^((?!ALOG).)*$')).has('code',textRegex('^((?!(g|G)etIntField).)*$'))
.functions()
.functionToLocationStr()
.dedup()
    """

    query5 = """
getCallsToRegex(".*(g|G)etIntField.*")
.statements()
.out("REACHES")
.statements()
.has('code' , textRegex(".*(malloc|memcpy).*") )
.functions()
.functionToLocationStr()
    """
    for r in db.runGremlinQuery(query5):
        print(r)

