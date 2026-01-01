import os
import pkgutil
import sys
import importlib.util
import time
if not hasattr(pkgutil, "get_loader"):
    def get_loader(name):
        # Special-case __main__ (running script): __spec__ is often None
        if name == "__main__":
            return getattr(sys.modules.get("__main__"), "__loader__", None)

        try:
            spec = importlib.util.find_spec(name)
        except (ValueError, ImportError):
            return None

        return spec.loader if spec else None

    pkgutil.get_loader = get_loader

import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Regexp
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY
VERIFY_CODE = os.environ.get("VERIFY_CODE")
sender = os.environ.get("GMAIL_USER")
password = os.environ.get("GMAIL_APP_PASSWORD")
receiver = sender
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        time.sleep(0.2)
        return render_template("homepage.html")

    username = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    if phone == "" or phone == None:
        phone = "User prefered not to give"
    message = request.form.get("message", "").strip()

    if not username or not email or not message:
        flash("Please fill in Name, Email, and Message.")
        time.sleep(0.2)
        return redirect(url_for("home"))

    body = (
        f"Username: {username}\n"
        f"Email: {email}\n"
        f"Phone Number: {phone}\n\n"
        f"Message:\n{message}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = f"New Message from {username}!"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            flash("✅ Your message has been sent successfully!")
            return redirect(url_for("home"))
    except Exception as e:
        flash("❌ Failed to send email. Please try again.")
        time.sleep(0.2)
        return redirect(url_for("home"))

@app.route("/about")
def about():
    time.sleep(0.2)
    return render_template("about.html")

@app.route("/project")
def project():
    time.sleep(0.2)
    return render_template("projects.html")
@app.route("/?!?")
def secret():
    return render_template("secret.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/skills")
def skills():
    time.sleep(0.2)
    return render_template("skills.html")

# message sending
@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "GET":
        time.sleep(0.2)
        return render_template("message.html")

    username = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    if phone == "" or phone == None:
        phone = "User prefered not to give"
    message = request.form.get("message", "").strip()

    if not username or not email or not message:
        flash("Please fill in Name, Email, and Message.")
        time.sleep(0.2)
        return redirect(url_for("contact"))

    body = (
        f"Username: {username}\n"
        f"Email: {email}\n"
        f"Phone Number: {phone}\n\n"
        f"Message:\n{message}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = f"New Message from {username}!"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            flash("✅ Your message has been sent successfully!")
            time.sleep(0.2)
            return redirect(url_for("contact"))
    except Exception as e:
        flash("❌ Failed to send email. Please try again.")
        time.sleep(0.2)
        return redirect(url_for("contact"))

# verify page
class VerifyForm(FlaskForm):
    password = StringField("Enter Code here:", validators=[DataRequired()])
    button = SubmitField("Enter")

@app.route("/verify/",methods=["GET","POST"])
def verify():
    form = VerifyForm()
    lang = request.form.get("lang") or request.args.get("lang")

    if lang == "de":
        form.password.label.text = "Passwort"
        form.button.label.text = "Bestätigen"
    elif lang == "zh":
        form.password.label.text = "密码"
        form.button.label.text = "验证"
    else:
        form.password.label.text = "Password"
        form.button.label.text = "Verify"

    if form.validate_on_submit():
        if form.password.data == VERIFY_CODE:
            print("VALIDATED ✅", form.password.data)
            time.sleep(2)
            return redirect(url_for("path", lang=lang))
        else:
            print("NOT VALID ❌", form.errors)
            flash("Incorrect code. Please try again.", "danger")
            return redirect(url_for("verify", lang=lang))
    return render_template("verify.html", form=form)


@app.route("/path")
def path():
    time.sleep(1)
    return render_template("path.html")


if __name__ == "__main__":
    app.run(debug=True)
