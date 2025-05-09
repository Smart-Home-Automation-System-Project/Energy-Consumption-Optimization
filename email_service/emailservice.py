import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
load_dotenv()

def send_email(receiver_name, receiver_email, device_name, anomaly_count, power_excess):
    """
    Sends an email about device anomalies detected.

    :param receiver_name: Name of the recipient.
    :param receiver_email: Email address of the recipient.
    :param device_name: Name of the device with anomalies.
    :param anomaly_count: Number of anomalies detected.
    :param power_excess: Total excess power consumption.
    """
    # Get email credentials from environment variables
    sender_email = os.getenv("SMTP_SERVER_USERNAME")
    password = os.getenv("SMTP_SERVER_PASSWORD")

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Energy Consumption Anomaly Alert - {device_name}"

    # Build the HTML email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="background-color: #FF4444; color: white; text-align: center; padding: 20px;">
                    <h1 style="margin: 0;">Energy Consumption Anomaly Alert</h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px;">
                    <p style="font-size: 16px;">Dear <strong>{receiver_name}</strong>,</p>
                    <p style="font-size: 16px;">We have detected anomalies in energy consumption for your device.</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr style="background-color: #f8f8f8;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Device Details</th>
                            <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Statistics</th>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #ddd;">
                                <div>
                                    <h3 style="margin: 0; font-size: 16px;">{device_name}</h3>
                                    <p style="margin: 5px 0; color: #666;">Number of Anomalies: {anomaly_count}</p>
                                </div>
                            </td>
                            <td style="padding: 15px; text-align: right; border-bottom: 1px solid #ddd; font-weight: bold;">
                                Total Excess: {power_excess:.2f} W
                            </td>
                        </tr>
                    </table>

                    <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-top: 20px; border: 1px solid #ffeeba;">
                        <h3 style="margin: 0 0 10px 0; color: #856404;">Recommendation</h3>
                        <p style="margin: 5px 0; font-size: 14px;">Please check your device for any malfunctions or irregular usage patterns. Consider scheduling maintenance if issues persist.</p>
                    </div>

                    <p style="font-size: 14px; margin-top: 20px;">If you need assistance understanding these anomalies, please contact our support team.</p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 12px;">
                    <p style="margin: 0;">&copy; 2024 Energy Consumption Monitor. All rights reserved.</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    message.attach(MIMEText(html_content, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(os.getenv("SMTP_SERVER_HOST"), 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return "Anomaly alert email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        raise Exception("Failed to authenticate with SMTP server. Please check your email credentials in the .env file and ensure you're using an App Password if using Gmail.")
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

# For testing - commented out to prevent accidental sends
# send_email("John Doe", "john@example.com", "AC Unit 1", 5, 1250.75)