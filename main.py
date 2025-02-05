from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
from forms import ReservationForm
import webbrowser
from os import getenv

app = Flask(__name__)
app.secret_key = getenv('FLASK_KEY')

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
        message = f"Seats: {seats}\nDate: {date}\nTime: {time}"
        send_whatsapp_message(message)
        return redirect(url_for("home"))
    return render_template("index.html", form=form)

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ReservationForm()
    if form.validate_on_submit():
        name = form.name.data
        seats = form.seats.data
        date = request.form["date"]
        time = form.time.data
        email = form.email.data
        message = form.message.data
        msg = f"Name: {name}\nSeats: {seats}\nDate: {date}\nTime: {time}\nEmail: {email}\nMessage: {message}"
        # send_whatsapp_message(msg)
        webbrowser.open_new_tab("https://web.whatsapp.com/send/?phone=584147415933&text&type=phone_number&app_absent=0")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

# def send_whatsapp_message(message):
#     number = getenv("PHONE_NUMBER")
#     try:
#         if environ['DISPLAY']:
#             pywhatkit.sendwhatmsg_instantly(number, message)
#         else:
#             print("No se puede enviar el mensaje de WhatsApp: DISPLAY no está definido")
#     except Exception as e:
#         print("Error al enviar el mensaje de WhatsApp:", e)

if __name__ == "__main__":
    app.run(debug=True, port=5000)