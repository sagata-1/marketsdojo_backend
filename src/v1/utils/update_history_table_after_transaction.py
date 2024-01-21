'''
Here I am not going to write the code for the function first. I am going write the API/the contract first.
And if the implementer codes to satisfy the post conditions @ensures clauses and the caller of this function satisfies 
the preconditions @requires clauses, then the function will work as expected. FOllow the contract and everything will go smoothly

Now your API can be free flowing english like Java API or it can be more formal like OAS or OSU CSE Components
What are the inputs and what is my function going to do with those inputs?

Simple english: After a user buys an asset, I need to log this entry into the history table and importantly I need to log the amount he invested in the given transaction. 
More formally:
@requires @param user_id is the id of the user who is buying 
@requires @param symbol is the symbol of the asset the user is buying
@requires @param transaction_price is the current market price at the time the user clicked buy
@requires @param quantity is the number of units of the asset the user is buying
@requires @param transaction_time is the date-time stamp when the user user clicked buy 
@requires @param transaction_time IS_VALID i.e. market is open for that given asset
@ensures HISTORY[invested_amt_per_transaction] = MULTIPLY(@param price, @param quantity)
@ensures new history table = old history table + current transaction record
@returns true if HISTORY table was successfully updated, false otherwise

def update_history_table_after_buy(user_id, symbol, transaction_price, quantity, transaction_time):
	implementer_responsibility_satisfied=false
	try:
		//calculate the amount the user is investing in this transaction
		invested_amount = transaction_price*quantity
		//Use SQL query to INSERT a new record in the HISTORY table where the "invested_amount_per_transaction" column is set to
		//above calculated invested_amount and other values for other columns are copied from what is passed into this function
		implementer_responsibility_satisfied=true
	catch Exception as e:
		print(e)
	
	return implementer_responsibility_satisfied

'''

def update_history_table_after_transaction(user_id, data):
    return {"code": 302, "message": "to be implemented", "data": {}}