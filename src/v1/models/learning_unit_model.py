from utils.database import db

class LearningUnitModel(db.Model):
    __tablename__ = 'learning_units'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)
    learning_unit_number = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False)