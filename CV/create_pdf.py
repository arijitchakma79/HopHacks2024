from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(data, filename="attention_summary_report.pdf"):
    """
    Generate a PDF summary report from the session data.
    :param data: A dictionary of the data to be included in the PDF.
    :param filename: The filename for the generated PDF.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "User Attention Summary Report")

    # Write attention data
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Session Summary:")

    c.drawString(50, height - 120, f"Overall Attention Score: {data['avg_attention_score'] * 100:.2f}%")
    c.drawString(50, height - 140, f"Total Frames Processed: {data['total_frames']}")
    c.drawString(50, height - 160, f"Total Face Detected Frames: {data['face_detected_frames']} ({(data['face_detected_frames'] / data['total_frames']) * 100:.2f}%)")
    c.drawString(50, height - 180, f"Total Movements Detected: {data['total_movements']}")
    c.drawString(50, height - 200, f"Overall Motion Intensity: {data['total_motion_intensity']:.2f}")

    c.save()
    print(f"PDF report '{filename}' created successfully.")
