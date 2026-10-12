# 📦 Online Courier Tracking System

A web-based courier management and tracking application built using Python Flask, SQLite, HTML, CSS, and JavaScript. The system allows users to register, log in, book courier services, track shipments, and view delivery information. It also provides an administrative interface for managing courier bookings, delivery statuses, and GPS location details.

---

## 📌 Project Overview

The Online Courier Tracking System aims to improve logistics efficiency through digital tracking and information management.

The application provides a convenient way for users to book couriers and track their delivery progress. Administrators can manage shipments and update delivery information through a centralized dashboard.

## ✨ Features

### 👤 User Features
- User registration and login
- User dashboard
- Book courier services
- Generate unique tracking IDs
- Track courier status
- View courier details
- Access GPS location information when available

### 🛠️ Admin Features
- Administrator login
- Admin dashboard
- View courier bookings
- Update courier delivery status
- Manage courier tracking information
- View latitude and longitude when available
- Open courier coordinates on Google Maps
### 🚚 Driver Dashboard

The Driver Dashboard helps delivery personnel manage assigned courier deliveries and update delivery progress.

- Driver dashboard to view assigned courier deliveries
- View courier tracking IDs and shipment details
- Access pickup and delivery addresses
- Update delivery status as the shipment progresses
- Share current GPS location when location access is enabled
- View latitude and longitude coordinates
- Open the current location in Google Maps
- Track delivery progress from pickup to final destination

**Note:** Driver dashboard features depend on the functionality implemented in the application. Live GPS tracking requires the driver's device to share location data with the system.

### 📍 GPS Tracking
- Browser-based GPS location access
- Display latitude and longitude when location permission is granted
- View available coordinates on Google Maps

**Note:** GPS tracking depends on location permission, device capabilities, and the availability of location data. Browser-based GPS does not automatically provide a courier's live location unless the courier's device is actively sharing it with the application.

---

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Client-side interactions |
| Browser Geolocation API | GPS location access |
| Google Maps | Display geographic coordinates |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📂 Project Structure

```text
Online_Courier_Tracking_System/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── database/
│   └── courier.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── book_courier.html
│   ├── track_courier.html
│   ├── courier_details.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── error.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        └── logo.png
```

*The structure above is illustrative. Your actual files may differ.*

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Advithareddy/Online-Courier-Tracking-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Online-Courier-Tracking-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize the Database

Ensure that the application creates the required SQLite database tables during startup. Check `database.py` and `app.py` for the database initialization logic.

If your application already initializes the database automatically, no additional command is necessary.

### 6. Run the Application

```bash
python app.py
```

### 7. Open the Website

Open your browser and visit:

```text
http://127.0.0.1:5000
```

The application will run locally on your computer.

---

## 🔄 Application Workflow

1. A user registers and logs in.
2. The user opens the dashboard.
3. The user books a courier by entering the required shipment details.
4. The system generates a unique tracking ID.
5. The user enters the tracking ID to check courier information and status.
6. The administrator views courier bookings and updates delivery statuses.
7. GPS coordinates can be displayed when location data is available.

---

## 🎯 Project Objectives

- Digitize courier booking and tracking operations.
- Provide a centralized interface for courier management.
- Improve access to shipment status information.
- Support GPS coordinate visualization when available.
- Improve logistics efficiency through digital tracking and information management.

---

## 🔒 Security and Privacy

- Do not commit real user passwords, personal addresses, or private shipment information.
- Do not publish secret keys or credentials.
- Use environment variables for sensitive configuration in production.
- Use appropriate password hashing and access controls before deploying the application publicly.
- Do not expose a development database containing real user information.

---

## 🚀 Future Enhancements

- Interactive map integration
- Improved live courier location sharing
- Email and SMS delivery notifications
- Shipment history and tracking timeline
- Delivery reports and analytics
- Responsive mobile-friendly interface
- Production deployment with secure configuration

---

## 👩‍💻 Author

**Advitha Reddy**

GitHub: [@Advithareddy](https://github.com/Advithareddy)

---

## 📜 License

This project was developed for educational and academic purposes.

A formal open-source license can be added if you choose to distribute the project under specific licensing terms.
