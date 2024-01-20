def get_total_invested_amt(portfolio_entries):
    """
        Calculate the total invested amount from a list of portfolio entries.
        
        :param portfolio_entries: A list of dictionaries, where each dictionary represents a portfolio entry 
                                  and has a key 'invested_amount' with a numeric value.
        :type portfolio_entries: list(dict), 'invested_amount' in portfolio_entries
        :type portfolio_entries[i]['invested_amount']: float
        :return: The sum of all 'invested_amount' values from the portfolio entries.
        :rtype: float
    """
    return sum(item["invested_amount"] for item in portfolio_entries)