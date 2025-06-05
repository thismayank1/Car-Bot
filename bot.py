from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
import os
from model import predict_car_price
from report import generate_pdf

app = Flask(__name__)
user_data = {}

# Sample car brand options
car_brands = [
    'Maruti', 'Hyundai', 'Honda', 'Toyota', 'Tata', 'Ford', 'Mahindra',
    'Skoda', 'Volkswagen', 'Renault', 'Chevrolet', 'BMW', 'Audi', 'Mercedes-Benz'
]

@app.route("/bot", methods=["POST"])
def bot():
    sender = request.form.get("From")
    msg = request.form.get("Body")
    response = MessagingResponse()
    msg_reply = response.message()

    if sender not in user_data:
        user_data[sender] = {"step": 0, "data": {}}

    step = user_data[sender]["step"]
    data = user_data[sender]["data"]

    if step == 0:
        brands_str = ', '.join(car_brands)
        msg_reply.body(f"Select your car brand from the following:\n{brands_str}")
        user_data[sender]["step"] = 1

    elif step == 1:
        selected_brand = msg.strip().capitalize()
        if selected_brand not in car_brands:
            msg_reply.body("❌ Invalid brand. Please select from:\n" + ', '.join(car_brands))
        else:
            data["brand_model"] = selected_brand.lower()
            msg_reply.body("Year of manufacture (e.g., 2018):")
            user_data[sender]["step"] = 2

    elif step == 2:
        try:
            data["year"] = int(msg)
            msg_reply.body("Kilometers driven (e.g., 42000):")
            user_data[sender]["step"] = 3
        except ValueError:
            msg_reply.body("Please enter a valid year (e.g., 2018):")

    elif step == 3:
        try:
            data["km_driven"] = int(msg)
            msg_reply.body("Fuel type (Diesel/Petrol/LPG/CNG):")
            user_data[sender]["step"] = 4
        except ValueError:
            msg_reply.body("Please enter a valid number of kilometers (e.g., 42000):")

    elif step == 4:
        data["fuel_type"] = msg.lower()
        msg_reply.body("Seller type (Individual/Dealer/Trustmark Dealer):")
        user_data[sender]["step"] = 5

    elif step == 5:
        data["seller_type"] = msg.lower()
        msg_reply.body("Transmission type (Manual/Automatic):")
        user_data[sender]["step"] = 6

    elif step == 6:
        data["transmission"] = msg.lower()
        msg_reply.body("Owner type (First Owner/Second Owner/Third Owner/Fourth & Above Owner/Test Drive Car):")
        user_data[sender]["step"] = 7

    elif step == 7:
        data["owner"] = msg.lower()
        msg_reply.body("Mileage (kmpl):")
        user_data[sender]["step"] = 8

    elif step == 8:
        try:
            data["mileage"] = float(msg)
            msg_reply.body("Engine CC:")
            user_data[sender]["step"] = 9
        except ValueError:
            msg_reply.body("Please enter a valid mileage (e.g., 18.5):")

    elif step == 9:
        try:
            data["engine"] = float(msg)
            msg_reply.body("Max Power (bhp):")
            user_data[sender]["step"] = 10
        except ValueError:
            msg_reply.body("Please enter a valid engine CC (e.g., 1200):")

    elif step == 10:
        try:
            data["max_power"] = float(msg)
            msg_reply.body("Number of seats:")
            user_data[sender]["step"] = 11
        except ValueError:
            msg_reply.body("Please enter a valid max power (e.g., 80):")

    elif step == 11:
        try:
            data["seats"] = int(msg)

            # Predict car price
            predicted_price = predict_car_price(data)

            # Generate and send PDF report
            pdf_path = generate_pdf(data, predicted_price, image_path=None)

            # Update your ngrok
            pdf_url = ' https://31de-103-101-119-106.ngrok-free.app/download/' + pdf_path
            msg_reply.body(f"✅ Estimated Car Price: ₹{predicted_price:,.2f}\nDownload your report PDF:")
            msg_reply.media(pdf_url)

            # Reset
            user_data.pop(sender)
        except ValueError:
            msg_reply.body("Please enter a valid number of seats (e.g., 5):")

    return str(response)

@app.route("/download/<filename>")
def download_pdf(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
