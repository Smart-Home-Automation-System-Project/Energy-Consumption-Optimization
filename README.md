# Energy Consumption Optimization

## Overview
The Energy Consumption Optimization part aims to monitor and optimize energy usage in the house. It provides real-time analytics, anomaly detection, and predictive modeling to help users manage their energy consumption effectively.

## Features
- Real-time energy monitoring
- Anomaly detection for devices
- Historical data analysis
- Energy consumption forecasting
- Scheduling of tasks for energy optimization
- User-friendly web dashboard
- Daily cloud backup to Firebase at midnight

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- SQLite3
- Flask
- Pandas
- Prophet
- PyFlink

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Energy-Consumption-Optimization.git
   cd Energy-Consumption-Optimization
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Run the database setup script to create the necessary tables:
   ```bash
   python database/create_database.py
   ```

5. **Configure environment variables:**
   - Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   SMTP_SERVER_HOST=smtp.your-email-provider.com
   SMTP_SERVER_USERNAME=your_email@example.com
   SMTP_SERVER_PASSWORD=your_email_password
   
   # Firebase credentials
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   FIREBASE_APP_ID=your_app_id
   ```

## Running the Application

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **Access the dashboard:**
   - Open your web browser and go to link.

## Usage
- Use the dashboard to monitor real-time energy consumption.
- Set up scheduled tasks for devices to optimize energy usage.
- Review historical data and predictions to make informed decisions.
- All data is automatically backed up to Firebase cloud storage at midnight each day.