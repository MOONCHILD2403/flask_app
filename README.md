# Flask Sentiment Analysis App

## Overview

This Flask application provides a simple sentiment analysis tool using TextBlob. Users can register, log in, analyze text, and view their profile dashboard.

## Architecture

The application is built using Flask, a lightweight web framework for Python. MongoDB is used for database connectivity, storing user data. TextBlob is utilized for sentiment analysis, providing subjectivity and polarity scores for text input.

## API Endpoints

- `/`: Home page
- `/login`: User login page
- `/register`: User registration page
- `/profile`: User profile page
- `/analyze`: Text analysis page

## Instructions for Running Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/flask_app.git
   ```

2. **Install Dependencies**:
   ```bash
   cd flask_app
   pip install -r requirements.txt
   ```

3. **Set Up Configuration**:
   - edit the setup.json file in the project , replace "your_mongodb_connection_string" and "your_jwt_secret_key" with your actual MongoDB connection string and JWT secret key.
   - Ensure your MongoDB server is running <ins>**locally**</ins> and is accessible and change app_secret_key only if you have one. 

4. **Run the Application**:
   ```bash
   python main.py
   ```
   The application will be accessible at `http://localhost:5000`.

5. **Access the Application**:
   Open a web browser and navigate to `http://localhost:5000` to use the application.

## Usage

- **Registration**: Visit `/register` to create a new account.
- **Login**: Visit `/login` to log in to your account.
- **Text Analysis**: Visit `/analyze` to perform sentiment analysis on text inputs.
- **Dashboard**: Visit `/profile` to view your user dashboard and profile information or to update it.

## Dependencies

- Flask
- Flask_Bcrypt
- Flask_JWT_Extended
- Flask_PyMongo
- Requests
- textblob

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Author

- **Name**: Yashas Bajaj
- **Mail**: yashasbajaj2403@gmail.com


