from application.mongo import Connection
from flask import jsonify


class APIManager(object):
    
    @staticmethod
    def index():
        """
        API Manager Index Page
        :return:
        """
        return jsonify(
            status=200,
            detail="Welcome to Social Manager API",
            services=[{"source": "Twitter", "url": "/api/v1/twitter"}]
        ), 200


class TwitterAPI(object):
    
    @staticmethod
    def index():
        """
        Twitter API Index Page
        :return:
        """
        return jsonify(
            status=200,
            detail="Twitter API Index",
            services=[
                {
                    "name": "Listener",
                    "url": "/api/v1/twitter/search/{KEYWORD-TO-SEARCH}",
                    "util": "/api/v1/twitter/keywords"
                },
                {
                    "name": "Tweet Discover",
                    "url": "/api/v1/twitter/tweet/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                },
                {
                    "name": "Friends Discover",
                    "url": "/api/v1/twitter/friends/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                },
                {
                    "name": "Follower Discover",
                    "url": "/api/v1/twitter/follower/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                }
            ]
        ), 200
    
    @staticmethod
    def get_keywords():
        """
        Return the list of all available keywords
        :return: Json
        """
        return jsonify(status=200,
                       keywords=Connection.Instance().db.twitter.find({"source": "listener"}).distinct("keywords")), 200
    
    @staticmethod
    def search(keyword, page=1):
        """
        Get all tweets from a given keyword with pagination support.
        :param keyword: Keyword to search
        :param page: Page Number
        :return:
        """
        n_result = 10
        page = int(page)
        result = list(Connection.Instance().db.twitter.find(
            {
                "keywords": keyword,
                "source": "listener"
            },
            {
                "_id": False,
                "created": False,
                "keywords": False,
                "source": False
            }).skip((page-1)*n_result).limit(n_result))
        
        page_size = len(result)
        
        return jsonify(
            status=200,
            page_size=page_size,
            page=page,
            result=[data['data'] for data in result],
            next="/api/v1/twitter/search/python/%s" % str(page + 1) if page_size == n_result else None,
            before="/api/v1/twitter/search/python/%s" % str(page - 1) if page > 1 else None
        ), 200

    @staticmethod
    def get_users():
        """
        Return list of users fetched
        :return: Json
        """
        return jsonify(status=200,
                       users=Connection.Instance().db.twitter.find({"user": {"$ne": None}}).distinct("user")), 200