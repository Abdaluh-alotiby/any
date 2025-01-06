import os
from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Load email credentials from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")  # Environment variable for email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Environment variable for email password


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return jsonify({"error": "Invalid location data"}), 400

        # Generate the Google Maps link
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        # Prepare the email content
        subject = "User Location"
        body = (
            f"User's location:\n"
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"
            f"Google Maps: {maps_link}"
        )
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_USER

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")