from neo4j import GraphDatabase
import pandas as pd

class Neo4ia:
    def startSession(url,username,password):
        gdb = GraphDatabase.driver(url,auth=(username,password))
        return gdb.session()

    def stopSession(session):
        session.close()

    def queryToDataFrame(session,query):
        df = pd.DataFrame()
        for row in session.run(query):
            rowDict = {}
            for key in row.keys():
                rowDict[key] = row[key]
            df = df.append(rowDict,ignore_index=True)
        return df

    def queryToObject(session,query):
        result = []
        for row in session.run(query):
            rowDict = {}
            for key in row.keys():
                rowDict[key] = row[key]
            result.append(rowDict)
        return result