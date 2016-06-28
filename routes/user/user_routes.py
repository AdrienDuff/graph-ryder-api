from routes.user.user_getter import GetUser, GetUserHydrate, GetUsers
from routes.user.user_aggregations import CountUsersByTimestamp
from routes.user.user_interaction import ShortestPathBetweenUsers


def add_user_routes(api):
    # Getters
    api.add_resource(GetUsers, '/users')
    api.add_resource(GetUser, '/user/<int:user_id>')
    api.add_resource(GetUserHydrate, '/user/hydrate/<int:user_id>')

    # Count
    api.add_resource(CountUsersByTimestamp, '/users/count/timestamp')

    # Work in progress
    api.add_resource(ShortestPathBetweenUsers, '/user/shortestPath/<int:user1_id>/<int:user2_id>/<int:max_hop>')

    # todo GetUserType
    # todo GetUsersByType moderators, ...