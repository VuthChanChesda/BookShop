

# **BookShop - Django E-Commerce Platform**

Welcome to the **BookShop** project! This platform allows users to browse and purchase books. Users can sign up, sign in, customize their profiles, and proceed to checkout.

---

## **Features**

- **User Authentication:** Users can sign up, sign in, and manage their sessions.
- **Profile Management:** Users can update their name and address.
- **Shopping Cart:** Users can add books to their shopping cart.
- **Checkout Process:** Users can proceed with the purchase and send their order to the delivery company.

---

## **Prerequisites**

Before running the project, make sure you have the following installed on your machine:

- **Python** (3.6+)
- **Django** (3.2+)
- **SQLite** (comes with Django for database)
- **pip** (Python package manager)

---

## **Getting Started**

Follow the steps below to get your local copy of the project running.

### **1. Clone the Repository**

Copy the following command to clone the project:

```bash
git clone https://github.com/VuthChanChesda/BookShop.git
```

### **2. Navigate to the Project Folder**

Copy the command below to navigate into the project directory:

```bash
cd BookShop
```

### **3. Set Up a Virtual Environment**

It’s best practice to use a virtual environment. Run the following commands:

- On Windows:

  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### **4. Install Dependencies**

Run the following command to install all required Python packages:

```bash
pip install -r requirements.txt
```

### **5. Set Up the Database**

Run migrations to set up the database:

```bash
python manage.py migrate
```

### **6. Create a Superuser (Optional)**

You can create an admin superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the superuser account.

### **7. Run the Development Server**

Finally, run the development server to start the project:

```bash
python manage.py runserver
```

Your site should now be accessible at `http://127.0.0.1:8000/`.

---

## **Usage**

- **Sign up**: Create a new account by providing your name, email, and password.
- **Sign in**: Log into the site to access your profile and shopping cart.
- **Manage Profile**: Update your personal details and address.
- **Browse Books**: Explore the books available for purchase.
- **Add to Cart**: Add items to your cart for checkout.
- **Checkout**: Complete your purchase by providing a shipping address.

---

## **Contributing**

Feel free to fork the repository and submit pull requests if you want to contribute to the project. If you encounter any issues or have suggestions for improvement, please open an issue.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Contact**

For any questions or feedback, feel free to reach out to me via GitHub or email.



