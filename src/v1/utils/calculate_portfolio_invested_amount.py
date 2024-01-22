from models.history_model import HistoryModel
from utils.database import db

def calculate_portfolio_invested_amount(symbol, user_id):
    """
    Calculates the total invested amount for a specific symbol and user.

    :param symbol: The asset symbol to query in the history table.
    :type symbol: str
    :param user_id: The ID of the user.
    :type user_id: int
    :return: Total invested amount for the given symbol and user.
    :rtype: float
    """
    return db.session.query(db.func.sum(HistoryModel.invested_amount_per_transaction)).filter_by(symbol=symbol, user_id=user_id).scalar()
