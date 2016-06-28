from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class CountAllPost(Resource):
    def get(self):
        req = "MATCH (:post) RETURN count(*) AS nb_posts"
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse([result.single()['nb_posts']], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountPostByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:AUTHORSHIP]->(:post) RETURN count(*) AS nb_posts" % author_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse([result.single()['nb_posts']], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountPostsByTimestamp(Resource):
    def get(self):
        req = "MATCH (n:post) RETURN n.timestamp AS timestamp ORDER BY timestamp ASC"
        req += addargs()
        result = neo4j.query_neo4j(req)
        users = []
        count = 1
        for record in result:
            users.append({"count": count, "timestamp": record['timestamp']})
            count += 1
        return makeResponse(users, 200)
