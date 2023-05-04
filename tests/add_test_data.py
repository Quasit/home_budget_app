from datetime import datetime

def add_test_data():
    from script.models import db, User, Budget, AllowedUsers, Category, Expense, UsedBy
    
    # Test users
    user1 = User(username='test_user', email='test@email.com', virtual=False)
    user1.set_password('test')

    user2 = User(username='second_test_user', email='test2@email.com', virtual=False)
    user2.set_password('test2')

    db.session.add(user1)
    db.session.add(user2)

    db.session.flush()


    # Test budgets
    budget1 = Budget(name='test_budget_1', description='test_budget_1_description', owner_id=user1.id)

    budget2 = Budget(name='test_budget_2', description='test_budget_2_description', owner_id=user2.id)

    db.session.add(budget1)
    db.session.add(budget2)

    db.session.flush()

    # Test user allowance : budget1: user1(editor=True), user2(editor=False) | budget2: user2(editor=True)
    budget1_allowed1 = AllowedUsers(budget_id=budget1.id, user_id=user1.id, editor=True)
    budget1_allowed2 = AllowedUsers(budget_id=budget1.id, user_id=user2.id, editor=False)

    budget2_allowed1 = AllowedUsers(budget_id=budget2.id, user_id=user2.id, editor=True)

    db.session.add_all([budget1_allowed1, budget1_allowed2, budget2_allowed1])

    db.session.flush()

    # Test categories / only for budget 1

    category1 = Category(name='test_category1', description='test_category_1_description', budget_id=budget1.id, color='#ffffff')
    category2 = Category(name='test_category2', description='test_category_2_description', budget_id=budget1.id, color='#000000')

    db.session.add(category1)
    db.session.add(category2)

    db.session.flush()

    # Test expenses only / for budget 1

    date1 = datetime.strptime('2022-12-31', '%Y-%m-%d').date()
    date2 = datetime.strptime('2022-12-30', '%Y-%m-%d').date()
    date3 = datetime.strptime('2022-06-30', '%Y-%m-%d').date()
    date4 = datetime.strptime('1999-01-01', '%Y-%m-%d').date()

    expense1 = Expense(name='test_expense1', description='test_expense_1_description', budget_id=budget1.id,
                            category_id=category1.id, date=date1, amount='100.01', payer=user1.id)
    
    expense2 = Expense(name='test_expense2', description='test_expense_2_description', budget_id=budget1.id,
                            category_id=category1.id, date=date2, amount='50.00', payer=user2.id)
    
    expense3 = Expense(name='test_expense3', description='test_expense_3_description', budget_id=budget1.id,
                            category_id=category2.id, date=date3, amount='30.00', payer=user1.id)
    
    expense4 = Expense(name='test_expense4', description='test_expense_4_description', budget_id=budget1.id,
                            category_id=category1.id, date=date4, amount='2000.00', payer=user1.id)
    
    expense5 = Expense(name='test_expense5', description='test_expense_5_description', budget_id=budget1.id,
                            category_id=category1.id, amount='150.00', payer=user2.id)
    
    expense6 = Expense(name='test_expense6', description='test_expense_6_description', budget_id=budget1.id,
                            category_id=category2.id, amount='180.00', payer=user1.id)
    
    expense7 = Expense(name='test_expense7', description='test_expense_7_description', budget_id=budget1.id,
                            category_id=category2.id, amount='200.00', payer=user2.id)
    
    expenses = [expense1, expense2, expense3, expense4, expense5, expense6, expense7]

    db.session.add_all(expenses)

    db.session.flush()

    # Test UsedBy records / only for budget 1
    # Expense 1 (payer: User1) - Used_by: User1
    # Expense 2 (payer: User2) - Used_by: User2
    # Expense 3 (payer: User1) - Used_by: User1
    # Expense 4 (payer: User1) - Used_by: User1, User2
    # Expense 5 (payer: User2) - Used_by: User1
    # Expense 6 (payer: User1) - Used_by: User2
    # Expense 7 (payer: User2) - Used_by: User1, User2

    
    used_by_1 = UsedBy(expense_id=expense1.id, user_id=user1.id)  # Expense 1

    used_by_2 = UsedBy(expense_id=expense2.id, user_id=user2.id)  # Expense 2

    used_by_3 = UsedBy(expense_id=expense3.id, user_id=user1.id)  # Expense 3

    used_by_4 = UsedBy(expense_id=expense4.id, user_id=user1.id)  # Expense 4
    used_by_5 = UsedBy(expense_id=expense4.id, user_id=user2.id)  # Expense 4

    used_by_6 = UsedBy(expense_id=expense5.id, user_id=user1.id)  # Expense 5

    used_by_7 = UsedBy(expense_id=expense6.id, user_id=user2.id)  # Expense 6

    used_by_8 = UsedBy(expense_id=expense7.id, user_id=user1.id)  # Expense 7
    used_by_9 = UsedBy(expense_id=expense7.id, user_id=user2.id)  # Expense 7

    used_by_list = [used_by_1, used_by_2, used_by_3, used_by_4,
                    used_by_5, used_by_6, used_by_7, used_by_8, 
                    used_by_9]
    
    db.session.add_all(used_by_list)

    db.session.flush()


    db.session.commit()