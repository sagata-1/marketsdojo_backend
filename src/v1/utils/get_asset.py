from models.portfolio_model import PortfolioModel

def get_asset(symbol, user_id, asset_type):
    """
    Retrieves the first asset matching the given criteria from the PortfolioModel.

    :type symbol: str
    :param symbol: The symbol of the asset.

    :type user_id: int
    :param user_id: The user's ID.

    :type asset_type: str
    :param asset_type: The type of the asset.

    :rtype: PortfolioModel or None
    :return: The first asset found that matches the criteria or None if no match is found.
    """
    return PortfolioModel.query.filter_by(symbol=symbol, user_id=user_id, asset_type=asset_type).first()