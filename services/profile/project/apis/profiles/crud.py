from project import db
from project.apis.models import Profile


def get_all_profiles():
    return Profile.query.all()


def get_profile_by_user_id(user_id):
    return Profile.query.fiter_by(user_id=user_id).first()


def add_profile(
    user_id,
    first_name,
    last_name,
    gender=None,
    birth_date=None,
    blood_group=None,
    about=None,
):
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birth_date=birth_date,
        blood_group=blood_group,
        about=about,
    )
    db.session.add(profile)
    db.session.commit()
    return profile


def update_profile(
    profile,
    first_name,
    last_name,
    gender=None,
    birth_date=None,
    blood_group=None,
    about=None,
):
    profile.first_name = first_name
    profile.last_name = last_name
    profile.gender = gender
    profile.birth_date = birth_date
    profile.blood_group = blood_group
    profile.about = about
    db.session.commit()
    return profile


def delete_profile(profile):
    db.session.delete(profile)
    db.session.commit()
    return profile
