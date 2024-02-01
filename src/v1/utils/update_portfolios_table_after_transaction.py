from models.portfolio_model import PortfolioModel
from utils.get_asset import get_asset
from utils.database import db
from utils.calculate_portfolio_invested_amount import calculate_portfolio_invested_amount

def update_portfolios_table_after_transaction(data, user, asset):
    """
    Updates the portfolios table after a transaction (buy or sell) is made.

    :type data: dict
    :param data: The transaction data containing symbol, quantity, action, and asset_type.

    :type user: User
    :param user: The user performing the transaction.

    :type asset: dict
    :param asset: The asset involved in the transaction.

    :rtype: dict
    :return: A response dictionary with status code, message, and data.
    """
    symbol = data.get("symbol").upper()
    num_shares = data.get("quantity")
    action = data.get("action").lower()
    asset_type = data.get("asset_type")
    user_id = user.id
    response = {"code": 200, "message": "Success", "data": {}}
    asset_exists = get_asset(symbol, user_id, asset_type)
    if action == "buy":
        if not asset_exists:
            try:
                new_portfolio_entry = PortfolioModel(
                user_id=user_id,
                name=asset["name"],
                symbol=symbol,
                invested_amount=calculate_portfolio_invested_amount(symbol, user_id),
                quantity=num_shares,
                asset_type=asset_type
                )
                db.session.add(new_portfolio_entry)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
        else:
            try:
                asset_exists.quantity += num_shares
                asset_exists.invested_amount = calculate_portfolio_invested_amount(symbol, user_id)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
    else:
        if asset_exists.quantity - num_shares == 0:
            try:
                db.session.delete(asset_exists)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": {}}
        else:
            try:
                asset_exists.quantity -= num_shares
                asset_exists.invested_amount = calculate_portfolio_invested_amount(symbol, user_id)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": {}}
    return response