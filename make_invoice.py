from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_invoice(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # 1. Header (Simulating a generic supplier)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, "GLOBAL PACKAGING SOLUTIONS LTD.")
    c.setFont("Helvetica", 10)
    c.drawString(50, 735, "123 Industrial Park, Guangdong, CN")
    c.drawString(450, 750, "INVOICE #99283")
    c.drawString(450, 735, "Date: 2024-12-01")

    # 2. The "Trap" Data (Mixed Products & Packaging)
    # Note: We want the AI to ignore the "Cotton T-Shirt" and extract the boxes.
    data = [
        ("Item Description", "Qty", "Unit Price", "Total"),
        ("Men's Cotton T-Shirt (Black/L)", "500", "$4.50", "$2,250.00"),
        ("Corrugated Box - 12x12x12 (Single Wall)", "500", "$0.85", "$425.00"),
        ("Poly Mailer 10x13 (White/Self-Seal)", "1000", "$0.12", "$120.00"),
        ("Kraft Tape (Reinforced) - 3 inch", "20", "$5.00", "$100.00"),
        ("Shipping Label 4x6 (Roll of 500)", "10", "$8.00", "$80.00"),
    ]

    # 3. Draw Table
    y = 650
    c.setFont("Helvetica-Bold", 12)
    # Draw headers
    c.drawString(50, y, data[0][0])
    c.drawString(300, y, data[0][1])
    c.drawString(350, y, data[0][2])
    c.drawString(450, y, data[0][3])
    
    y -= 20
    c.line(50, y+10, 500, y+10) # Line under header
    
    c.setFont("Helvetica", 11)
    for row in data[1:]:
        y -= 20
        c.drawString(50, y, row[0])
        c.drawString(300, y, row[1])
        c.drawString(350, y, row[2])
        c.drawString(450, y, row[3])

    c.save()
    print(f"✅ Generated {filename}")

if __name__ == "__main__":
    create_dummy_invoice("sample_invoice.pdf")