from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Replace these with your email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "alotibyabdallh@gmail.com"
EMAIL_PASSWORD = "jiry jnrr cipm edap"


@app.route("/")
def index():
    # Serve the HTML template
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return jsonify({"error": "Invalid location data"}), 400

        # Prepare the email content
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
    app.run(debug=True,host='0.0.0.0')