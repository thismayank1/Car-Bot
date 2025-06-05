from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data, price, image_path=None):
    filename = f"{data['brand_model'].replace(' ', '_')}_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Car Price Prediction Report")

    c.setFont("Helvetica", 12)
    y = 730
    line_height = 20

    details = {
        "Brand": data.get('brand_model', ''),
        "Year": data.get('year', ''),
        "KMs Driven": data.get('km_driven', ''),
        "Fuel Type": data.get('fuel_type', ''),
        "Seller Type": data.get('seller_type', ''),
        "Transmission": data.get('transmission', ''),
        "Owner Type": data.get('owner', ''),
        "Mileage": f"{data.get('mileage', '')} kmpl",
        "Engine": f"{data.get('engine', '')} CC",
        "Max Power": f"{data.get('max_power', '')} bhp",
        "Seats": data.get('seats', ''),
        "Predicted Price": f"₹{price:.2f}"
    }

    for key, val in details.items():
        c.drawString(100, y, f"{key}: {val}")
        y -= line_height

    if image_path:
        try:
            c.drawImage(image_path, 350, 550, width=200, height=150)
        except Exception:
            pass  # Ignore image errors silently

    c.save()
    return filename
