import json

# Taking User choice to know which operation to perform.
def user_choice(choice):
    print('\n')
    for key, value in choice.items():
        print(f"{key}. {value}")
    while True:
        try:

            opt = int(input(f'Enter which operation would you like to perform.\noperation: '))
            if opt in choice:
                return opt
            else:
                print("Invalid choice. Enter value from 1 to 7.")

        except ValueError:
            print("Invalid choice. Enter Integer.")

#Save the updates into json file
def save_file(expenses):
    with open('expenses.json', 'w') as e:
        json.dump(expenses, e, indent=2)

#Selecting the expense for updating or deleting.
def select_expense(expenses):
    view_expenses(expenses)
    cat = input("Enter the category in which you expense is present: ").strip().title()
    while cat not in expenses:
        cat = input("The category is not present in the expenses. Please enter again: ").strip().title()
    des = input("Enter the description in which your expense is present:  ").strip().title()
    while des not in expenses[cat]:
        des = input("The description is not present in the expenses. Please enter again: ").strip().title()

    for index, exp in enumerate(expenses[cat][des], start=1):
        print(f"{index}. {exp}")

    while True:
        try:
            exp_number = int(input("Enter the index number of the expense you wish to edit: "))
            if (exp_number > 0) and (exp_number <= len(expenses[cat][des])):
                break
            print("You have entered a number which is not present in the index. Please enter again.")
        except ValueError:
            print("You need to enter only a number.")

    return cat, des, exp_number

#Validating the expense is a number or not
def get_expense_amount():
    while True:
        try:
            expense = float(input("Enter the amount of the expense: "))
            if expense <= 0:
                print("An expense must be greater than 0. Please try again.")
            else:
                break
        except ValueError:
            print("The number is invalid. Try again")

    return expense




# Adding expenses into the tracker.
def add_expenses(cat, des, exp, expenses):

    if cat not in expenses:
        expenses[cat] = {}
    if des not in expenses[cat]:
        expenses[cat][des] = []

    expenses[cat][des].append(exp)
    save_file(expenses)

#Viewing all the expenses entered into the tracker.
def view_expenses(expenses):
    if expenses:
        print(f"{'Category':<15}{'Description':<20}{'Expense':>10}")
        print("-" * 45)
        for cat in expenses:
            for des in expenses[cat]:
                for exp in expenses[cat][des]:
                    print(f"{cat:<15}{des:<20}{exp:>10}")
    else:
        print("There are no expenses entered into the tracker.")

#Total expenditure
def total_expenses(expenses):
    if expenses:
        amount = 0
        for cat in expenses:
            for des in expenses[cat]:
                for exp in expenses[cat][des]:
                    amount+=exp

        print(f"Total expenses incurred: {amount}")
    else:
        print("There are no expenses entered into the tracker.")

#Expenditure for each category
def total_expense_category(expenses):
    if expenses:
        for key in expenses:
            print(key)
        req_cat = input("Enter the category you need expenses for: ").title()
        if req_cat in expenses:
            print(f"Category: {req_cat}")
            print(f"{'Description':<20}{'Total':>10}")
            print("-"*30)
            amount = 0
            for des in expenses[req_cat]:
                sub_total = 0
                for exp in expenses[req_cat][des]:
                    sub_total+=exp
                print(f"{des:<20}{sub_total:>10}")
                amount+=sub_total
            print("-"*30)
            print(f"{'Total':<20}{amount:>10}")
        else:
            print(f"The category {req_cat} not available in tracker.")
    else:
        print("There are no expenses entered into the tracker.")

#Deleting a particular expense as per user choice
def delete_expense(expenses):
    if expenses:
        cat, des, exp_number = select_expense(expenses)
        expenses[cat][des].pop(exp_number-1)

        #removing empty descriptions and categories
        for cate in list(expenses.keys()):
            for desc in list(expenses[cate].keys()):
                if not expenses[cate][desc]:
                    del expenses[cate][desc]
            if not expenses[cate]:
                del expenses[cate]

        save_file(expenses)

    else:
        print("There are no expenses entered into the tracker.")


# Updating a particular expense as per user choice
def update_expense(expenses):
    if expenses:
        cat, des, exp_number = select_expense(expenses)
        expense = get_expense_amount()

        expenses[cat][des][exp_number-1] = expense
        save_file(expenses)

    else:
        print("There are no expenses entered into the tracker.")


#Program starts from here

tracker_close = 0
#expenses = {}
choice = {1: "Add Expense", 2: "View Expenses", 3: "Show total Expenses",
          4: "Show Expenses by Category", 5: "Delete Expense", 6: "Update Expense",7: "Exit"}

prev_tracker = input("Do you want to continue with previous tracker? y/n: ").lower()
while True:
    if prev_tracker == 'y':
        try:
            with open('expenses.json', 'r') as e:
                expenses = json.load(e)
        except FileNotFoundError:
            print('The file "expenses.json" is not found.')
            expenses = {}
        break

    elif prev_tracker == 'n':
        expenses = {}
        break
    else:
        prev_tracker = input("Wrong choice selected. Please select a valid choice.a y/n: ").lower()

while not tracker_close:

    operation = user_choice(choice)



    if operation == 1:
        print("Add Expense")
        category = input("Enter the category of the expense: ").strip().title()
        while category.strip() == '':
            category = input("Please enter a valid category for the expense: ").strip().title()
        description = input("Enter the description of the expense: ").strip().title()
        while description.strip() == '':
            description = input("Please enter a valid description for the expense: ").strip().title()
        expense = get_expense_amount()

        add_expenses(category, description, expense, expenses)

    elif operation == 2:
        print("View Expenses")
        view_expenses(expenses)

    elif operation == 3:
        print("Show total Expenses")
        total_expenses(expenses)


    elif operation == 4:
        print("Show Expenses by Category")
        total_expense_category(expenses)

    elif operation == 5:
        print("Delete Expense")
        delete_expense(expenses)

    elif operation == 6:
        print("Update Expense")
        update_expense(expenses)

    elif operation == 7:
        save_file(expenses)
        tracker_close = 1
        print("Exit")
        print("Exiting from the tracker.")
