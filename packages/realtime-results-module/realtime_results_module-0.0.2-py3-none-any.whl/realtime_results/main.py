import random
from typing import List, Dict, Any

from graphdb import GraphDb
from graphdb.connection import GraphDbConnection

import redis


class RealtimeResults:
    """This class will be as entry point"""

    def __init__(
        self, graph_connection: GraphDbConnection, redis_connection: redis.StrictRedis
    ):
        """Assumption service that include this module already create connection
        then passing that connection here, no need create new connection
        :param graph_connection: object graphdb connection
        """
        self.redis = redis_connection
        self.graph = GraphDb.from_connection(graph_connection)

    def homepage_recommendation(self) -> List[Dict[str, Any]]:
        """Calculate data for homepage recommendation
        :return: none
        """
        mock_data = [
            {
                "id": random.randint(1, 1_000),
                "recommendation": "recommendation_{}".format(random.randint(1, 1_000)),
            }
            for i in range(1, 51)
        ]
        return mock_data

    def homepage_cluster_category(self) -> List[Dict[str, Any]]:
        """Calculate data for homepage cluster category
        :return: none
        """
        mock_data = [
            {
                "id": random.randint(1, 1_000),
                "cluster_category": "cluster_category_{}".format(
                    random.randint(1, 1_000)
                ),
            }
            for i in range(1, 51)
        ]
        return mock_data

    def ranking(self):
        """Calculate data for ranking
        :return: none
        """
        mock_data = [
            {
                "id": random.randint(1, 1_000),
                "ranking": "ranking_{}".format(random.randint(1, 1_000)),
            }
            for i in range(1, 51)
        ]
        return mock_data
