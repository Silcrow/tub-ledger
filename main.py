from financial.accounting import Category, Account, print_balance_sheet


if __name__ == "__main__":

    '''assume user creates categories'''
    assets = Category('Assets')
    current_assets = Category('Current Assets', parent=assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    e_savings = Category('E-Savings', parent=current_assets, description='1M insured')
    fixed_assets = Category('Fixed Assets', parent=assets, description='Cannot liquidate in 1y')
    liabilities = Category('Liabilities')

    '''assume user creates accounts'''
    # Traditional Savings accounts
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    bkk_bank = Account('BKK Bank', 90744, category=traditional_savings)
    kt_bank = Account('KT Bank', 42287, category=traditional_savings)
    gh_bank = Account('GH Bank (partnered savings)', 19377, category=traditional_savings, remarks='50% of 38,754')
    baac_bank = Account('BAAC Bank (partnered savings)', 9915.5, category=traditional_savings, remarks='50% of 23,231')

    # E-Savings accounts
    g_wallet = Account('G-wallet (paotang)', 0, category=e_savings, remarks='KTBank')
    kpp_dime = Account('KPP Dime (high-yield)', 30000, category=e_savings)
    lhb_you = Account('LHB You (high-yield)', 10000, category=e_savings)

    # Fixed Assets accounts
    gh_bank_fd = Account('GH Bank 3-year Fixed Deposit (since 23M02)', 300000, category=fixed_assets,
                         remarks='2.25% semiannual')
    real_estate_equity = Account('Real estate partnership equity', 250000, category=fixed_assets,
                                 remarks='50% of the 500,000 down payment of 2.2M Baht house')
    maxvalu_fl3 = Account('MaxValu FL3', 300000, category=fixed_assets)
    midsoi_fl4 = Account('MidSoi FL4 (co-own sis)', 150000, category=fixed_assets, remarks='50% of 300,000')
    midsoi_fl2 = Account('MidSoi FL2 (co-own sis)', 115000, category=fixed_assets, remarks='50% of 230,000')

    # Liabilities accounts
    mortgage = Account('1.7M Mortgage (for the partnership property)', 480465.59, category=liabilities,
                       remarks='50% of 960,931.18')

    '''display each'''
    # print(assets.calculate_value())
    # print(liabilities.calculate_value())

    '''display as json'''
    # assets_dict = assets.to_dict()
    # print(json.dumps(assets_dict, indent=4, sort_keys=False, ensure_ascii=False))

    '''display as balance sheet'''
    print_balance_sheet(assets, liabilities)

    # TODO each time category or account object is created, save it as record in csv.
    # TODO now create a a function that would read from the csv's and python print a json version of the balance sheet.

