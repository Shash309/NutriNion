# NutriNion 🥗

A Django-based food tracking application that helps users monitor their nutritional intake and maintain a healthy diet.

## 🌟 Features

- **Food Management**
  - Add and categorize food items
  - View comprehensive food database
  - Track nutritional information

- **Food Logging**
  - Log daily food consumption
  - Track calories, proteins, fats, and carbohydrates
  - View detailed nutritional breakdown

- **User Authentication**
  - Secure registration and login
  - Personalized food logs
  - Protected user data

- **Nutritional Information**
  - Real-time data from Nutritionix API
  - Detailed nutrient breakdown
  - Daily nutritional tracking

## 🛠️ Technical Stack

- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap
- **External API**: Nutritionix API
- **Authentication**: Django's built-in auth system

## 📋 Prerequisites

- Python 3.x
- MySQL
- pip (Python package manager)
- Git

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shash309/nutrinion.git
   cd nutrinion
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   ```sql
   CREATE DATABASE nutrinion;
   ```

5. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your Nutritionix API credentials:
     ```
     NUTRITIONIX_API_KEY=your_api_key
     NUTRITIONIX_APP_ID=your_app_id
     ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## 💻 Usage

1. Register a new account or login
2. Add food items to the database
3. Log your daily food consumption
4. Track your nutritional intake

## 🔒 Security Features

- Secure password handling
- Protected routes
- SQL injection prevention
- XSS protection

## 📊 Database Structure

The application uses several key models:
- **User**: Django's built-in user model
- **Food**: Stores food items and nutritional information
- **FoodCategory**: Categorizes food items
- **FoodLog**: Records user's food consumption

## 🔄 API Integration

The application integrates with the Nutritionix API to fetch accurate nutritional information for food items. This integration is handled through a utility function that makes API calls and processes the response.

## 🎯 Future Enhancements

- Mobile application
- Advanced analytics
- Meal planning features
- Social sharing capabilities
- Barcode scanning for food items
- Custom recipe creation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Shashwat Sharma - Initial work

## 🙏 Acknowledgments

- Nutritionix API for providing nutritional data
- Django community for the amazing framework
- Bootstrap for the beautiful UI components
