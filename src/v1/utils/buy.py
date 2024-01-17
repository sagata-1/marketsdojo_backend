'''
@returns true if the buy was successful, false otherwise

def buy(user_id, reamining request body params):
	implementer_responsibility_satisfied=false
	boolean implementer_responsibility_1_satisfied=update_history_table_after_buy(pass in params from above method signature)
	boolean implementer_responsibility_2_satisfied=update_portfolios_table_after_buy("")
	implementer_responsibility_satisfied=implementer_responsibility_1_satisfied AND implementer_responsibility_2_satisfied
return implementer_responsibility_satisfied

'''
def buy(user_id, data):
    return insert_history_table_after_buy(user_id, data) and update_portfolios_table_after_buy(user_id, data)