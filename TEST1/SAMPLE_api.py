from flask import Flask
from flask_restful import Resource, reqparse ,Api

TGS = Flask(__name__)
api = Api(TGS)

articles = [
    {
        "service_name": "apache2",
        "service_status": "UP",
        "host_name": "host1"
    },
    {
        "service_name": "rabbitmq",
        "service_status": "UP",
        "host_name": "host2"
    },
    {
        "service_name": "postgresql",
        "service_status": "UP",
        "host_name": "host3"
    }
]

class Article(Resource):
    def get(self, service_name):
        for article in articles:
            if(service_name == article["service_name"]):
                return article, 200
        return "service not found", 404

    def post(self, service_name):
        parser = reqparse.RequestParser()
        parser.add_argument("service_status")
        parser.add_argument("host_name")
        args = parser.parse_args()

        for article in articles:
            if(service_name == article["service_name"]):
                return "service_name  {} already exists".format(service_name), 400

        article = {
            "service_name": service_name,
            "service_status": args["service_status"],
            "host_name": args["hostname"]
        }
        articles.append(article)
        return article, 201

    def put(self, service_name):
        parser = reqparse.RequestParser()
        parser.add_argument("service_status")
        parser.add_argument("host_name")
        args = parser.parse_args()

        for article in articles:
            if(service_name == article["service_name"]):
                article["service_status"] = args["service_status"]
                article["host_name"] = args["host_name"]
                return article, 200

        article = {
            "service_name": service_name,
            "service_status": args["service_status"],
            "host_name": args["host_name"]
        }
        articles.append(article)
        return article, 201

    def delete(self, service_name):
        global articles
        articles = [article for article in articles if article["service_name"] != service_name]
        return "{} is deleted.".format(service_name), 200

api.add_resource(Article, "/service_name/<string:service_name>")

TGS.run(debug=True,port=8080)
