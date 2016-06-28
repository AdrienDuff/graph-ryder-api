from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse


class GetUser(Resource):
    def get(self, user_id):
        req = "MATCH (find:user {uid: %d}) RETURN find" % user_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse([result.single()['find'].properties], 200)
        except ResultError:
            return makeResponse("ERROR : Cannot find user with uid: %d" % user_id, 204)


class GetUserHydrate(Resource):
    def get(self, user_id):
        # Get user properties
        req = "MATCH (find:user {uid: %d}) RETURN find" % user_id
        result = neo4j.query_neo4j(req)
        user = result.single()['find'].properties
        # Get user's posts
        req = "MATCH (find:user {uid: %d})" % user_id
        req += " MATCH (find)-[:AUTHORSHIP]->(p:post)"
        req += ' RETURN p.pid AS p_id, p.title AS p_title, p.timestamp AS p_time'
        result = neo4j.query_neo4j(req)
        posts = []
        posts_id = []

        for record in result:
            try:
                if record['p_id'] and record['p_id'] not in posts_id:
                    post = {}
                    post['pid'] = record['p_id']
                    post['title'] = record['p_title']
                    post['timestamp'] = record['p_time']
                    posts.append(post)
                    posts_id.append(post['pid'])
            except KeyError:
                pass
        # Get user's comments
        req = "MATCH (find:user {uid: %d})" % user_id
        req += " MATCH (find)-[:AUTHORSHIP]->(c:comment)"
        req += " OPTIONAL MATCH (c)-[:COMMENTS]->(p:post)"
        req += ' RETURN c.cid AS c_id, c.subject AS c_subject, c.timestamp AS c_time, p.pid AS parent_id'
        result = neo4j.query_neo4j(req)
        comments_id = []
        comments = []

        for record in result:
            try:
                if record['c_id'] and record['c_id'] not in comments_id:
                    comment = {}
                    comment['cid'] = record['c_id']
                    comment['subject'] = record['c_subject']
                    comment['timestamp'] = record['c_time']
                    comment['parent_id'] = record['parent_id']
                    comments.append(comment)
                    comments_id.append(comment['cid'])
            except KeyError:
                pass

        try:
            user
        except NameError:
            return makeResponse("ERROR : Cannot find user with uid: %d" % user_id, 204)
        user['posts'] = posts
        user['comments'] = comments
        return makeResponse([user], 200)


class GetUsers(Resource):
    def get(self):
        req = "MATCH (find:user) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        users = []
        for record in result:
            users.append(record['find'].properties)
        return makeResponse(users, 200)
