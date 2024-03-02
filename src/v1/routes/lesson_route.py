from . import lesson_route_1
#from flask import request, make_response, jsonify
from services.lesson.get_lessons import get_lessons
from utils.login_required import login_required


@lesson_route_1.route("/v1/courses/<int:course_id>", methods=["GET"])
@login_required
def index(access_token,course_id):
    """
    Handles requests to the lession API endpoint.

    :type access_token: str
    :param access_token: The access token used for authentication.

    :type course_id: str
    :param course_id: The course_id used to find lessons related to that course.

    :rtype: Response
    :return: A Flask response object containing the API response and status code.
    """
    #return f"Course ID: {course_id}, Lesson ID: {lesson_id}, Sub Lesson ID: {sub_lesson_id}"
    return get_lessons(course_id)