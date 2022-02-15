from flask import request
from flask_restx import Namespace, Resource, fields

from project.apis.decorators import token_required
from project.apis.profiles.crud import (
    add_profile,
    delete_profile,
    get_all_profiles,
    get_profile_by_user_id,
    update_profile,
)

profile_namespace = Namespace("profiles")

profile_model = profile_namespace.model(
    "Profile",
    {
        "user_id": fields.Integer(readOnly=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "gender": fields.String,
        "birth_date": fields.Date,
        "blood_group": fields.String,
        "about": fields.String,
    },
)

parser = profile_namespace.parser()
parser.add_argument("Authorization", location="headers")


class ProfileList(Resource):
    @token_required
    @profile_namespace.expect(parser, validate=True)
    @profile_namespace.marshal_with(profile_model, as_list=True)
    def get(self):
        """Returns all profiles of budget tracker users"""
        if ProfileList.get.owner_role != "admin":
            profile_namespace.abort(403, "Access Denied")
        return get_all_profiles(), 200

    @token_required
    @profile_namespace.expect(parser, profile_model, validate=True)
    @profile_namespace.response(201, "Profile for user <user_id> was added.")
    @profile_namespace.response(400, "Unable to create profile.")
    @profile_namespace.response(400, "Profile already exists.")
    def post(self):
        """Create a profile for a budget tracker user"""
        post_data = request.get_json()
        user_id = ProfileList.post.owner_id
        first_name = post_data.get("first_name")
        last_name = post_data.get("last_name")
        gender = post_data.get("gender")
        birth_date = post_data.get("birth_date")
        blood_group = post_data.get("blood_group")
        about = post_data.get("about")

        profile = get_profile_by_user_id(user_id=user_id)
        if profile is not None:
            profile_namespace.abort(400, "Profile already exists.")
        profile = add_profile(
            user_id=ProfileList.post.owner_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date,
            blood_group=blood_group,
            about=about,
        )
        response_object = {"message": f"Profile for user {profile.user_id} was added."}
        return response_object, 201


class Profile(Resource):
    @token_required
    @profile_namespace.expect(parser, validate=True)
    @profile_namespace.marshal_with(profile_model)
    def get(self, user_id):
        """Retrive budget tracker profile by user id"""
        return get_profile_by_user_id(user_id=user_id), 200

    @token_required
    @profile_namespace.expect(parser, profile_model, validate=True)
    @profile_namespace.response(200, "Profile update for user <user_id>.")
    @profile_namespace.response(400, "Unable to update profile.")
    @profile_namespace.response(404, "Profile does not exitsts.")
    def put(self, user_id):
        """Updates the budget tracker profile of an user"""
        put_data = request.get_json()
        user_id = Profile.put.owner_id
        first_name = put_data.get("first_name")
        last_name = put_data.get("last_name")
        gender = put_data.get("gender")
        birth_date = put_data.get("birth_date")
        blood_group = put_data.get("blood_group")
        about = put_data.get("about")

        profile = get_profile_by_user_id(user_id=user_id)
        if profile is None:
            profile_namespace.abort(404, "Profile does not exitsts.")
        profile = update_profile(
            profile=profile,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date,
            blood_group=blood_group,
            about=about,
        )
        response_object = {"message": f"Profile updated for user {profile.user_id}"}
        return response_object, 200

    @token_required
    @profile_namespace.expect(parser, validate=True)
    @profile_namespace.response(204, "Profile for user <user_id> was deleted.")
    @profile_namespace.response(403, "Access Denied.")
    @profile_namespace.response(404, "Profile does not exitsts.")
    def delete(self, user_id):
        if user_id != Profile.delete.owner_id:
            profile_namespace.abort(403, "Access Denied.")
        profile = get_profile_by_user_id(user_id=user_id)
        if profile is None:
            profile_namespace.abort(404, "Profile does not exitsts.")
        profile = delete_profile(profile=profile)
        response_object = {
            "message": f"Profile for user {profile.user_id} was deleted."
        }
        return response_object, 204


profile_namespace.add_resource(ProfileList, "", endpoint="profile-list")
profile_namespace.add_resource(Profile, "/<int:user_id>", endpoint="profile")
