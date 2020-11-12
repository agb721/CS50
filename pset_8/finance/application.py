import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time

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
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, SUM (shares) as share_count FROM transactions WHERE user_id=:user_id GROUP BY symbol", user_id=session["user_id"])
    total_values = []
    expenses = 0
    for stock in stocks:
        dic = {}
        dic["symbol"] = stock["symbol"]
        quote = lookup(stock["symbol"])
        dic["price"] = quote["price"]
        dic["name"] = quote["name"]
        dic["total_value"] = quote["price"] * stock["share_count"]
        dic["shares"] = stock["share_count"]
        total_values.append(dic)

    balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])


    return render_template("index.html", anything=total_values, balance=balance[0]["cash"])

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("enter a symbol", 403)
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 403)
        # Get shares
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares need to be positive integers")
        price = quote["price"]
        total_cost = price*shares

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
        #return render_template("bought.html", anything=budget)
        budget = rows[0]["cash"]
        if total_cost > budget:
            return apology("insufficient funds", 403)

        timestamp = time.time()

        # Update database
        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
        total_cost=total_cost, user_id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (:user_id, :symbol, :shares, :price, :timestamp)",
        user_id=session["user_id"], symbol=symbol, shares=shares, price=price, timestamp=timestamp)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id=:user_id", user_id=session["user_id"])

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("enter a symbol", 403)

        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if quote is None:
            return apology("invalid symbol", 403)

        price = quote["price"]
        return render_template("quoted.html", price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure passowrds match
        elif not confirmation==password:
            return apology("password and confirmation must match", 403)

        # Query database for username to check if already taken
        taken = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(taken) > 0:
            return apology("username already taken", 403)

        # Password conditions: Password cannot be shorter than 4 chars + requires at least one number and a symbol
        # Inspired by: https://stackoverflow.com/questions/32874900/python-password-checker-numbers-and-symbols
        alpha = 0
        num = 0
        sym = 0

        for c in password:
            if c.isalpha():
                alpha += 1
            elif c.isdigit():
                num += 1
            else:
                sym += 1

        if len (password) < 4:
            return apology("password too short. Minimum length is 4")
        elif num == 0 and sym == 0:
            return apology("at least one symbol and one character required")


        # Create new user
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
        username=username, password=generate_password_hash(password))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """"Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("enter a symbol", 403)
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 403)
        # Get shares
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares need to be positive integers")
        price = quote["price"]
        total_sold = price*shares

        stocks = db.execute("SELECT symbol, SUM (shares) as share_count FROM transactions WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol)
        if len(stocks) < 1:
            return apology("make sure you own the stock you wish to sell", 400)
        # stocks = [{'symbol': 'AAPL', 'share_count': 9}, {'symbol': 'TSLA', 'share_count': 2}]
        if shares > int(stocks[0]["share_count"]):
            return apology("you cannot sell more shares than you own", 400)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        timestamp = time.time()

        # Update database
        db.execute("UPDATE users SET cash = cash + :total_sold WHERE id = :user_id",
        total_sold=total_sold, user_id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (:user_id, :symbol, :shares, :price, :timestamp)",
        user_id=session["user_id"], symbol=symbol, shares=-shares, price=price, timestamp=timestamp)


        return redirect("/")

    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
