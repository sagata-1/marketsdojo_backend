# test_course_service.py
import json
import pytest
from flask import Flask
from utils.database import db
from urllib.parse import quote_plus
from unittest.mock import MagicMock
from models.learning_unit_model import LearningUnitModel
from services.sub_lesson.get_sub_lesson import get_sub_lesson

encoded_password = quote_plus("gWd2fjODUxYvr9zL")

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= f"postgresql://postgres.ejinafkbyepfnqtgwstk:{encoded_password}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app
    return app

def test_get_sub_lesson(app):
    with app.test_request_context():
        # Sample data for testing
        course_id = 1
        lesson_id = 2
        sub_lesson_id = 3


        #Mocking the LearningUnitModel.query.filter_by method
        mock_query = MagicMock()
        LearningUnitModel.query.filter_by = mock_query
        mock_query.filter_by.return_value = LearningUnitModel(id=sub_lesson_id, content="Sample content", title="Sample Sub-Lesson")


        response = get_sub_lesson(course_id, lesson_id, sub_lesson_id)
        data = json.loads(response.get_data(as_text=True))
        print(f"Data: {data}")

        # Assert the expected data in the response
        assert data["code"] == 200
        assert data["message"] == "Success"
        assert data["data"]["sub_lesson_id"] == sub_lesson_id



