# sub_lesson_service.py
from utils.get_user_from_token import get_user_from_token
from models.learning_unit_model import LearningUnitModel
from flask import jsonify, make_response


def get_sub_lesson(course_id, lesson_id, sub_lesson_id):
    """
    Show list of all lessons based on lesson_id & course_id.

    :type course_id: str
    :param course_id: The course_id used to find lessons related to that course.

    :type lesson_id: str
    :param lesson_id: The lesson_id used to find sub-lessons related to that lesson.

    :type sub_lesson_id: str
    :param sub_lesson_id: The sub_lesson_id used to find a specefic sub-lesson by its id.

    :return: A Flask response object with lesson data and HTTP status code
    :rtype: tuple(dict, int)
    """
    response = {}
    code = 200
    serialized_sub_lesson = []
    sub_lesson = LearningUnitModel.query.filter_by(id=sub_lesson_id, parent_id=lesson_id).first()
    if sub_lesson and sub_lesson.parent_id:
        lesson = LearningUnitModel.query.filter_by(id=lesson_id, parent_id=course_id).first()
        if lesson and lesson.parent_id:
            course = LearningUnitModel.query.filter_by(id=course_id, parent_id=None).first()
            if course:
                serialized_sub_lesson = {"sub_lesson_id": sub_lesson.id,"content": sub_lesson.content,"sub_lesson_name": sub_lesson.title,"course": course.title ,"lesson": lesson.title }

    sub_lesson_data = {"code": 200, "message": "Success", "data": serialized_sub_lesson}
    response = jsonify(sub_lesson_data)
    return make_response(response, code)


