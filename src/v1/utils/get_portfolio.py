from models.portfolio_model import PortfolioModel

def get_portfolio(user_id):
    """
    Provide all portfolio entries for a given user.

    :param user_id: The user's ID
    :type user_id: int, > 0
    :return: A list of dictionaries, each representing a portfolio entry
    :rtype: list(dict)
    """
    portfolio_entries = PortfolioModel.query.filter_by(user_id=user_id).order_by(PortfolioModel.symbol).all()
    serialized_portfolio = [
        {
            "symbol": entry.symbol,
            "name": entry.name,
            "quantity": entry.quantity,
            "asset_type": entry.asset_type,
            "invested_amount": entry.invested_amount
        }
        for entry in portfolio_entries
    ]
    
    return serialized_portfolio