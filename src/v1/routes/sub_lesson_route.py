from . import sub_lesson_route_1
from services.sub_lesson.get_sub_lesson import get_sub_lesson
from utils.login_required import login_required


@sub_lesson_route_1.route("/v1/courses/<int:course_id>/lessons/<int:lesson_id>/sub_lessons/<int:sub_lesson_id>", methods=["GET"])
@login_required
def index(access_token,course_id, lesson_id, sub_lesson_id):
    """
    Handles requests to the lession API endpoint.

    :type access_token: str
    :param access_token: The access token used for authentication.

    :type course_id: str
    :param course_id: The course_id used to find lessons related to that course.

    :type lesson_id: str
    :param lesson_id: The lesson_id used to find sub-lessons related to that lesson.

    :type sub_lesson_id: str
    :param sub_lesson_id: The sub_lesson_id used to find a specefic sub-lesson by its id.

    :rtype: Response
    :return: A Flask response object containing the API response and status code.
    """
    #return f"Course ID: {course_id}, Lesson ID: {lesson_id}, Sub Lesson ID: {sub_lesson_id}"
    return get_sub_lesson(course_id, lesson_id, sub_lesson_id)