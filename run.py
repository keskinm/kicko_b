import os

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from sqlalchemy import and_

from models import encode_auth_token, decode_auth_token
from queries.common import add_row, delete_row, make_query, row_to_dict, update
from tables.professional.business import Business

from tables.professional.job_offers import JobOffers
from tables.professional.user import User

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app)


@app.route("/api/user", methods=["GET"])
def get_user():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        print("AUTH TOKEN NON VIDE")
        auth_token = auth_header.split(" ")[1]

        succeed, resp = decode_auth_token(auth_token, app.config.get("SECRET_KEY"))
        if succeed:
            user = make_query(User, filters=User.email == resp).first()
            response_object = {
                "status": "success",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "id": str(user.id),
                },
            }
            return make_response(jsonify(response_object)), 200
        response_object = {"status": "fail", "message": resp}
        return make_response(jsonify(response_object)), 401

    else:
        # @todo Why a double call everytime with the first one here?
        # Find why and then put fail and 401 response status
        response_object = {"status": "success", "message": "Provide a valid auth token."}
        return make_response(jsonify(response_object)), 200


@app.route("/api/get_business", methods=["POST"])
def get_business():
    input_json = request.get_json(force=True)
    user_id = input_json["user_id"]
    result = row_to_dict(make_query(Business, Business.user_id == user_id).first())
    result = jsonify(result)
    result.status_code = 200
    return result


@app.route("/api/update_business_fields", methods=["POST"])
def update_business_fields():
    input_json = request.get_json(force=True)
    business = make_query(Business, Business.user_id == input_json.pop("user_id")).first()
    update(business, input_json)
    result = jsonify({})
    result.status_code = 200
    return result


@app.route("/api/get_job_offers", methods=["POST"])
def get_job_offers():
    input_json = request.get_json(force=True)
    user_id = input_json["user_id"]
    result = make_query(JobOffers, JobOffers.user_id == user_id)
    result = [row_to_dict(o) for o in result]
    result = jsonify(list(result))
    result.status_code = 200
    return result


@app.route("/api/add_job_offer", methods=["POST"])
def add_job_offer():
    input_json = request.get_json(force=True)
    add_row(JobOffers, input_json)
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/delete_job_offer", methods=["POST"])
def delete_job_offer():
    input_json = request.get_json(force=True)
    user_id = input_json["user_id"]
    job_offer_id = input_json["id"]
    delete_row(JobOffers, [JobOffers.user_id == user_id, JobOffers.id == job_offer_id])
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/user_register", methods=["POST"])
def user_register():
    input_json = request.get_json(force=True)
    add_row(User, input_json)
    user_id = row_to_dict(make_query(User, User.email == input_json["email"]).first())
    add_row(Business, {"user_id": user_id["id"]})
    resp = jsonify({})
    resp.status_code = 200
    return resp


@app.route("/api/authentication-token", methods=["POST"])
def get_token():
    input_json = request.get_json(force=True)
    username = input_json["username"]
    password = input_json["password"]
    query_result = make_query(
        User, filters=and_(User.username == username, User.password == password)
    ).first()
    if query_result:
        token = encode_auth_token(username, app.config.get("SECRET_KEY"))
        result = jsonify({"token": token})
        result.status_code = 200
    else:
        result = jsonify({})
    return result


@app.route("/")
def home():
    return "home"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
