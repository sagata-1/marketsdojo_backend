# lesson_service.py
from models.learning_unit_model import LearningUnitModel
from flask import jsonify, make_response


def get_lessons(course_id):
    """
    Show list of all lessons based on course_id.

    :type course_id: str
    :param course_id: The course_id used to find lessons related to that course.

    :return: A Flask response object with lesson data and HTTP status code
    :rtype: tuple(dict, int)
    """
    response = {}
    code = 200
    cource = LearningUnitModel.query.filter_by(id=course_id, parent_id=None).first()
    if cource:
       lessons = LearningUnitModel.query.filter_by(parent_id=cource.id).all()
       course_lessons= [
         {
            "lesson_id": entry.id,
            "lesson_no": entry.learning_unit_number,
            "lesson_title": entry.title,
            "content": entry.content,
            "created_at": entry.created_at
        }
         for entry in lessons
      ]
    course_data={
       "course_id": cource.id,
       "course_no": cource.learning_unit_number,
       "course_title": cource.title,
       "created_at": cource.created_at,
       "lessons": course_lessons
    }
    course_result = {"code": 200, "message": "Success", "data": course_data}
    response = jsonify(course_result)
    return make_response(response, code)


