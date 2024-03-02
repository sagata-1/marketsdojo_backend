from models.game_monetary_account_model import GameMonetaryAccountModel,db


'''
    This function queries the game monetary account table by game id, to retrieve the game monetary accounts of a particular game, for all participants.
    Then, for each monetary account of that particular game identified by its game id, it updates the available balance by adding the balance increment to the available balance.
'''

def increment_available_balance_by_game_id(game_id,balance_increment):
    game_monetary_accounts=GameMonetaryAccountModel.query.filter_by(game_id=game_id).all()
    for game_monetary_account in game_monetary_accounts:
        game_monetary_account.available_balance+=balance_increment
        db.session.commit()
    return {"message":"Available balance incremented successfully"},200