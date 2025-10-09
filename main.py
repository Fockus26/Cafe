from flask import Flask, render_template, redirect, request
from datetime import datetime
from forms import ReservationForm
import urllib.parse
from os import getenv

app = Flask(__name__)
app.secret_key = getenv('FLASK_KEY')

WHATSAPP_NUMBER = getenv('WHATSAPP_NUMBER')

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming_soon.html")

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReservationForm()
    if request.method == "POST":
      seats = form.seats.data
      date = request.form["date"]
      time = form.time.data

      # Construimos el mensaje
      msg = f"☕ *New Reservation Request*\n\nSeats: {seats}\nDate: {date}\nTime: {time}"

      # Codificamos el mensaje para URL
      encoded_msg = urllib.parse.quote(msg)

      # Redirigimos a WhatsApp
      whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"
      return redirect(whatsapp_url)

    return render_template("index.html", form=form)

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ReservationForm()
    if request.method == "POST":
        name = form.name.data
        seats = form.seats.data
        date = request.form["date"]
        time = form.time.data
        email = form.email.data
        message = form.message.data

        msg = (
            f"📩 *New Contact / Reservation*\n\n"
            f"Name: {name}\nSeats: {seats}\nDate: {date}\nTime: {time}\n"
            f"Email: {email}\nMessage: {message}"
        )

        encoded_msg = urllib.parse.quote(msg)
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"
        return redirect(whatsapp_url)

    return render_template("contact.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
