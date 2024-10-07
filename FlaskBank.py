from flask import Flask, render_template, redirect, url_for, flash, request

app=Flask(__name__)
app.secret_key='clubdelapelea'

class Account:
    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance
        self.transactions = [f"Cuenta creada con saldo inicial de {initial_balance}"]

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Depósito: {amount}")

    def withdraw(self, amount):
        if self.balance >= amount and amount > 0:
            self.balance -= amount
            self.transactions.append(f"Retiro: {amount}")
        else:
            flash(f"Fondos insuficientes o cantidad inválida en la cuenta de {self.name}")

    def check_balance(self):
        return self.balance

    def generate_statement(self):
        return self.transactions

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, initial_balance):
        if name in self.accounts:
            flash("La cuenta ya existe")
        else:
            self.accounts[name] = Account(name, initial_balance)
            flash(f"Cuenta creada para {name} con saldo inicial de {initial_balance}")

    def transfer(self, from_account, to_account, amount):
        if from_account in self.accounts and to_account in self.accounts:
            if self.accounts[from_account].balance >= amount and amount > 0:
                self.accounts[from_account].withdraw(amount)
                self.accounts[to_account].deposit(amount)
                flash(f"Se ha transferido {amount} de {from_account} a {to_account}.")
            else:
                flash("Fondos insuficientes en la cuenta de origen")
        else:
            flash("Una o ambas cuentas no existen")
    def show_all_accounts(self):
        all_accs = [account for account in self.accounts]
        return all_accs

bank = Bank()

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        account = request.form['name']
        amount = float(request.form['initial_balance'])
        if account in bank.accounts:
            flash(f'la cuenta ya existe')
        else:
            bank.create_account(account, amount)
            flash(f'Se ha creado la cuenta de {account} con un saldo inicial de {amount}')
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/withdraw', methods=['GET','POST'])
def withdraw():
    accounts = bank.show_all_accounts()
    if request.method == 'POST':
        account = request.form['account']
        amount = float(request.form['amount'])
        if account in bank.accounts:
            bank.accounts[account].withdraw(amount)
            flash(f"Se ha retirado {amount} de la cuenta {account}")
        else:
            flash("La cuenta no existe")
        return redirect(url_for('index'))
    return render_template('withdraw.html', accounts=accounts)

@app.route('/deposit', methods=['GET','POST'])
def deposit():
    accounts = bank.show_all_accounts()
    if request.method == 'POST':
        account = request.form['account']
        amount = float(request.form['amount'])
        if account in bank.accounts:
            bank.accounts[account].deposit(amount)
            flash(f"Se ha retirado {amount} de la cuenta {account}")
        else:
            flash("La cuenta no existe")
        return redirect(url_for('index'))
    return render_template('deposit.html', accounts=accounts)

@app.route('/transfer', methods=['GET','POST'])
def transfer():
    accounts = bank.show_all_accounts()
    if request.method == 'POST':
        from_account = request.form['from_account']
        to_account = request.form['to_account']
        amount = float(request.form['amount'])
        if from_account in bank.accounts and to_account in bank.accounts:
            bank.transfer(from_account, to_account, amount)
        else:
            flash('La cuenta no existe')
        return redirect(url_for('index'))
    return render_template('transfer.html', accounts=accounts)

@app.route('/check_balance', methods= ['GET','POST'])
def check_balance():
    accounts = bank.show_all_accounts()
    if request.method == 'POST':
        account = request.form['account']
        if account in bank.accounts:
            balance = bank.accounts[account].check_balance()
            flash(f'El saldo de {account} es: {balance}')
        else:
            flash('La cuenta no existe')
        return redirect(url_for('index'))
    return render_template('check_balance.html', accounts=accounts)

@app.route('/generate_statement', methods= ['GET','POST'])
def generate_statement():
    if request.method == 'POST':
        account = request.form['account']
        if account in bank.accounts:
            transactions = bank.accounts[account].generate_statement()
            return render_template('statement.html', transactions=transactions, account=account)
        else:
            flash('La cuenta no existe')
        return redirect(url_for('index'))
    accounts = bank.show_all_accounts()
    return render_template('generate_statement.html', accounts=accounts)

if __name__ == "__main__":
    app.run(debug=True)
            