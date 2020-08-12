import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # current users id
    uid = session["user_id"]

    # query database for owned stock from current user
    stocks = db.execute("SELECT symbol, shares FROM portfolios WHERE user_id=:user_id ORDER BY symbol DESC", user_id=uid)

    # condition to check for user stocks
    if not stocks:
        return render_template("index.html", message="No stocks owned :(")

    # variable to hold total
    total = 0

    # update the dicts inside stock with current prices, etc
    for stock in stocks:
        stock.update({ "name": lookup(stock["symbol"])["name"] })
        price = lookup(stock["symbol"])["price"]
        stock.update({ "price": usd(price) })
        value = price * int(stock["shares"])
        stock.update({ "value": usd(value) })
        total = total + value

    # query database to get the current users total cash
    cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["cash"]

    # calculate total value of portfolio
    total = total + cash

    return render_template("index.html", stocks=stocks, cash=usd(cash), value=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # variables for symbol and number of shares to buy
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # check that user submitted values, and right values
        if not symbol:
            return apology("must provide stock symbol", 403)
        elif not shares or int(shares) <= 0:
            return apology("must provide number of shares to buy", 403)


        # checks the price of the stock, and calculates the resulting price to buy a specific number
        api_result = lookup(symbol)
        # conditions to check for 200
        if api_result == None:
            return apology("Something went wrong, please try again", 403)
        else:
            price = float(api_result["price"]) * int(shares)

        # check database for how much cash the user has
        user_cash = db.execute("SELECT cash FROM users WHERE id = :idnumber", idnumber=session["user_id"])[0]["cash"]

        #check to see if user can afford to buy
        if user_cash < price:
            return apology("Not enough cash to buy select number of shares", 403)

        # insert transaction into database
        db.execute("INSERT INTO transactions (user_id, type, symbol, shares, price) VALUES (:user_id, :trans_type, :symbol, :shares, :price)", user_id=session["user_id"], trans_type="purchase", symbol=symbol, shares=int(shares), price=price)

        # calcylate users new cash balance after the purchase of said stocks
        user_cash = user_cash - price
        #then update database
        db.execute("UPDATE users SET cash=:balance WHERE id=:user_id", user_id=session["user_id"], balance=user_cash)

        # then to updating the users portfolio
        portfolio = db.execute("SELECT shares FROM portfolios WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol)

        # check to see if user already have purchased these stocks
        if len(portfolio) == 1:
            #calculate and update info
            shares = portfolio[0]["shares"] + int(shares)
            db.execute("UPDATE portfolios SET shares=:shares WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol, shares=shares)
        # if user has not bought any previous shares of this stock
        else:
            db.execute("INSERT INTO portfolios (user_id, symbol, shares) VALUES (:user_id, :symbol, :shares)", user_id=session["user_id"], symbol=symbol, shares=int(shares))
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT datetime, type, symbol, shares, price FROM transactions WHERE user_id=:user_id ORDER BY datetime DESC", user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # variable to hold the text for the stocks symbol
        stock_symbol = request.form.get("symbol")

        # loopup for that particular symbol
        lookup_result = lookup(stock_symbol)

        # conditions to check if the result of the api call is either None or data to display
        if lookup_result is None:
            return apology("Something went wrong", 403)
        else:
            # Redirect user quoted page to display results
            return render_template("quoted.html", lookup_result=lookup_result)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # variables for useername and password
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must provide confirmation of password", 403)

        # ensure that password and confirmation is equal
        elif not confirmation == password:
            return apology("password and confirmation password must be the same", 403)

        # checks if username is already used in the sql database
        user_row = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(user_row) == 1:
            return apology("username already used", 403)

        # Insert username and hash of password into database, in the table: users
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        stocks = db.execute("SELECT symbol FROM portfolios WHERE user_id=:user_id ORDER BY symbol ASC", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # ensure submitted values
        if not symbol:
            return apology("you provide symbol", 403)
        elif int(shares) <= 0:
            return apology("Number of shares must be over 0", 403)

        # get users portfolio
        stocks = db.execute("SELECT shares FROM portfolios WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol)

        # calculate if user has enough shares to sell for that selected symbol
        if int(stocks[0]["shares"]) < int(shares) or len(stocks) != 1:
            return apology("you dont have enough shares", 403)

        # calculate the price of the number of stocks on the current market price
        price = lookup(symbol)["price"] * int(shares)

        # insert transaction
        db.execute("INSERT INTO transactions (user_id, type, symbol, shares, price) VALUES (:user_id, :trans_type, :symbol, :shares, :price)",
            user_id = session["user_id"],
            trans_type = "sell",
            symbol = symbol,
            shares = int(shares),
            price = format(price,".2f"))

        # current user cash balance
        cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["cash"]

        # new cash balance
        cash = cash + price

        # update cash balance
        db.execute("UPDATE users SET cash=:balance WHERE id=:user_id", user_id=session["user_id"], balance=cash)

        # get new ammount of shares of the stock
        shares = int(stocks[0]["shares"]) - int(shares)

        #update users portfolio
        db.execute("UPDATE portfolios SET shares=:shares WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol, shares=shares)

        return redirect("/")


@app.route("/wallet", methods=["GET", "POST"])
@login_required
def wallet():
    """Add more cash."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assign input to variable
        amount = request.form.get("amount")

        # Ensure cash amount was submitted
        if not amount:
            return apology("no amount of cash input", 403)

        # Query database to update user's cash amount
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id",
            user_id = session["user_id"],
            amount = amount)

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("wallet.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
