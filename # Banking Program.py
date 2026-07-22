# Banking Program
def Show_Balance():
    print(f"Your balance is ksh{balance:.2f}")

def Deposit():
    amount = float(input("Enter amount to be deposited: "))

    if amount < 0:
        print("Invalid amount entered")
        return 0
    else:
        return amount
    
def Withdraw():
    amount = float(input("Enter amount to be withdrawn: "))
    if amount > balance:
        print("Insufficient funds")
        return 0
    elif amount < 0:
        print("Amount must be greater than zero")
        return 0
    else:
        return amount

balance = float(0)
is_running = True

while is_running:
    print("Banking Program")
    print("1.Show Balance")
    print("2.Deposit")
    print("3.Withdraw")
    print("4.Exit")

    choice = input("Enter your choice(1-4): ")
    if choice == '1':
        Show_Balance()
    elif choice == '2':
        balance += Deposit()
    elif choice == '3':
        balance -= Withdraw()
    elif choice == '4':
        is_running = False
    else:
        print("Invalid choice, please try again.")

print("Thank you! Have a nice day!")