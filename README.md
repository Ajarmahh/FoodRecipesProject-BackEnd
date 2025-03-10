# 🍽️ Food Recipes Project - Backend

Welcome to the **Food Recipes Project Backend**! This is the backend service for a dynamic recipe recommendation platform, powered by AI. Users can search for recipes, get personalized suggestions, and manage their favorite dishes.  

## 🚀 Features  
- 🔍 **AI-Powered Recipe Recommendations** – Suggests recipes based on user preferences and available ingredients  
- 🔐 **JWT Authentication** – Secure user authentication for a personalized experience  
- 📚 **CRUD Operations** – Manage recipes, user data, and favorites efficiently  
- ⚡ **Fast & Scalable** – Optimized API performance with Flask and SQLite  
- 🌍 **RESTful API** – Seamless integration with the frontend application  

## 🛠️ Tech Stack  
- **Backend Framework:** Flask (Python)  
- **Database:** SQLite + SQLAlchemy ORM  
- **Authentication:** JWT  
- **API Integration:** AI-powered recipe recommendation system  
- **Deployment:** Docker (Optional)  

## 🛋️ Installation & Setup  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/Ajarmahh/FoodRecipesProject-BackEnd.git
cd FoodRecipesProject-BackEnd
```

2️⃣ **Create a Virtual Environment & Install Dependencies**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3️⃣ **Run the Application**  
```bash
python app.py
```

4️⃣ **Test the API**  
Use **Postman** or **cURL** to interact with the API and test endpoints.

## 🔗 API Endpoints  

| Method | Endpoint               | Description                           |
|--------|------------------------|---------------------------------------|
| GET    | `/recipes`             | Fetch all recipes                     |
| POST   | `/recipes`             | Add a new recipe                      |
| GET    | `/recipes/<id>`        | Fetch a single recipe by ID           |               
| DELETE | `/recipes/<id>`        | Delete a recipe                       |
| POST   | `/register`            | User registration (coming soon)       |          
| POST   | `/login`               | User authentication (JWT)(coming soon)|    
