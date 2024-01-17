'''
    def buy_api_controller(access_token):
	list1= buy_api_pre_conditions_satisfied()
	client_responsibility_satisfied=list1[0]
	server_response = list1[1]
	implementer_responsibility_satisfied=false
	if client_responsibility_satisfied:
		try:
			implementer_responsibility_satisfied=
			buy(user_id=get_user_id_from_access_token(access_token),request.json.get("symbol"), remaining input parameters of buy function)
		catch Exception as e:
			response_code=500
			server_response=e
	else if client_responsibility_satisfied AND not implementer_responsibility_satisfied:
		response_code =500
		server_response="Buy Unsuccesfull"
	else if client_responsibility_satisfied AND implementer_responsibility_satisfied:
		response_code=200 
		server_response="Buy Successful"
	else
		response_code=400
	return_list[0]=response_code
	return_list[1]=server_response
	
return return_list

'''