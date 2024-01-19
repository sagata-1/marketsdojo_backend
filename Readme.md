Correctness of software has been a fundamental and extensively researched topic in Computer Science and Software Engineering, and is often ignored in Industry.
Ensuring the correctness of software is not only the intellectual endevaor of a trained Engineer but it is crucial for building reliable, robust and secure systems. 
Formal methods aim to mathematically prove the the correctness of software with respect to a set of specifications. 
Another way to achieve this goal is the "Correct by Construction" approach which inolves designing software systems in a way that correctness is inherent in the design. 
This is achieved by using formal specifications, design patterns like SOLID, MVC, Encapsulation, SOC, and other engineering practices to minimize the chance of introducing errors. 

Given a method that has some precondtion, p and some post-condition q. The "correctness" of that function is determined by the truth value of the implication p-->q. 
If p-->q evaluates to true, your software is correct and is doing what is expected. In the canonical truth table seen in propositional logic, if p is false, p-->q is true
regardless of the truth value of q. If I make the promise that if it is sunny tomorrow I will take you to the beach, then if it is not sunny tomorrow the promise is true
regardless if we go to the beach or not. The promise is only broken if it is sunny tomorrow and we don't go to the beach. Then p is true, q is false and p-->q evaluates to false. So you're software is incorrect if the precondition of the method is satisfied but the postcondition is not. Therefore, we aim to achieve p=true and q=true.

Satisfying the precondition is the responsibility of the caller of the function, satisfying the post-condition is the responsibility of the implementer.

This codebase employs the Design-by-Contract paradigm of specifying method contracts using clauses that were used in OSU CSE Components before PyContracts was developed by MIT.Any developer working on this codebase must install PyContracts and first write the contract for each function using the @contract decorator before implementing the function. Then implement the contract to ensure it's post-condition is satisfied by your implementation.
During development, Use assert statement to explicitly check the preconditions and postcondtions are satisfied. Asserts are turned off in production so you need error handling functions.

Contracts should be comprehensively written using all or several of the clauses below that @contract decorator in "PyContracts" allows:-

1. Arguments (argname=clause):
Specifies the contract for a function argument.
Example: @contract(x='int,>=0')

2. Returns (returns=clause):
Specifies the contract for the return value of the function.
Example: @contract(returns='float,>0')

3. Ensures (ensures=clause):
Specifies a postcondition that must hold true after the function is executed.
Example: @contract(ensures='result > 0')

4. Requires (requires=clause):
Specifies a precondition that must be true before the function is executed.
Example: @contract(requires='x > 0')

5. Raises (raises=clause):
Specifies the conditions under which an exception is raised.
Example: @contract(raises='ValueError, msg.startswith("Invalid")')

6. Invariant (invariant=clause):
Specifies an invariant for a class. It defines a condition that must be true for the entire lifetime of the class.
Example: @contract(invariant='self.x > 0')

7.Old (old(argname)):
Represents the value of an argument as it was at the beginning of the function.
Example: @contract(x='int', ensures='x > old(x)')

8.New (new(argname)):
Represents the value of an argument as it is at the end of the function.
Example: @contract(x='int', ensures='x > new(x)')

9. ForAll (forall(argname=clause)):
Specifies a universally quantified contract. It asserts that the specified condition holds true for all elements in the argument.
Example: @contract(forall('x', 'x > 0'))
----
4 things need to happen when a user buy and/or sells an asset

1. After a user buys an asset	
	a) How does his invested amount for that given asset across previous transactions update?
	b) How does that users total invested amount, across all previous transactions, across all assets update? (may need new database table for this)
2. After a user sells an asset
	a) How does his invested amount for that given asset across previous transactions update?
	b) How does that users total invested amount, across all previous transactions, across all assets ? (may need new database table for this)
	
Lets start with 1 part a)
------
Q: What are some published best practice to follow that we to see how they relate to our use-case?
A:
1. Functions should not have multiple return statements. -use make_response to subvert this
2. Do not modify a container while you are iterating over it.
3. Do not use break statements
4. Use MVC pattern
-----
Q: As per the SOLID principle, what is the S? What is the single responsibility of this function?
A: You give me some information about what the user is buying and I update the relevant tables in the database to reflect the fact that he has bought this asset.

Which means ultimately the buy function needs to look like this. 

def buy():
	update table1
	update table2
	...
	update table_n
return xyz

Split and chain functions till each function does but one thing. Every file has only 1 function. 
It does not retrive user_id AND check for errors in the request payload, it does not update history table and portfolios table and cash table.

Q: How can you abide by the design-by-contract best practice for software engineering? Following traffic laws when driving a car.
A: Before coding the function write its contract. What does this function expect as inputs, what conditions are on the inputs, what does this function ensures
to be true. Use Pycontracts @contracts decorator to Fill in the following and then write code to fulfill this contract using assert statements. 

Preconditions: @requires What must be true before this function is called? What is the expectation of this function from the client?
Postconditions: @ensures What does this function gurantee? What is true after this function is called?
@Aliases - Does this function create any aliases?
@Updates
@returns
---
Design Considerations
	1. Delete time bought column from portfolios table as that is already in history table
	2. In HISTORY table rename stock_symbol to symbol for more generality 
	3. In PORTFOLIOS table rename type to asset_type for better description
	3. Error handling? - Create a function with boolean return, call that from another function - which is the controller.
	4. /v1/api/buy calls def buy_api_pre_conditions_satisfied(), if yes, calls def buy_api_get_user_id_from_access_token(), calls def buy_api()
	5. To eliminate the possibility of a bug in asset_type and symbol match we will not allow the user to select this from a dropdown, 
		it will come from the asset selection panel, therefore reducing the error handling code we need to write in backend by changing front end design.
	6. How will the database object be passed around? - It will be initialized in app.py and imported in __init__.py of the subfolder who's function needs it (utils)
---
routes folder: handles all incoming HTTP requests but the logic is written in the service folder
service folder - implements business logic for api folder
utils folder - has helper functions
---
