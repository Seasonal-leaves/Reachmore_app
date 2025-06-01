# Influencer Engagement & Sponsorship Coordination Platform

A web application built with Vue.js and Flask for managing influencer marketing campaigns. This platform supports three types of users — Admins, Sponsors, and Influencers — each with distinct roles and capabilities.

## 🔥 Features

### 👤 Authentication
- Secure signup and login
- JWT-based token authentication

### 🧑‍💼 Sponsor Features
- Create, edit, delete ad campaigns
- Search for influencers
- Send, edit, delete ad requests
- Negotiate and chat with influencers
- Track campaign budgets and performance
- View monthly reports

### 📢 Influencer Features
- View and search campaigns
- Send and delete ad requests
- Negotiate offers and communicate with sponsors
- Daily reminders for pending actions

### 🔧 Admin Features
- Accept or reject new sponsor registrations
- Flag suspicious users and campaigns
- Monitor system statistics through the admin dashboard

---

## 🛠️ Technologies Used

### Frontend:
- [Vue.js 3](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [BootstrapVue](https://bootstrap-vue.org/)
- Fetch API

### Backend:
- [Python Flask](https://flask.palletsprojects.com/)
- [Flask-Security](https://flask-security-too.readthedocs.io/) (with JWT)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/)

---

## 📁 Project Structure

```
/frontend         → Vue.js app with component-based structure
/backend          → Flask REST API with SQLAlchemy ORM
/database         → SQLite DB used for data storage
```

---

## 🚀 Getting Started

### 📦 Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

### 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Dashboards

- **Admin Dashboard**: View stats on users, campaigns, ad requests, and flagged entities.
- **Sponsor Dashboard**: Visual campaign analytics including budget, ad request statuses, and influencer performance.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributions

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 👨‍💻 Developed By

- [Your Name]  
- Contact: [your.email@example.com]  
- Organization: [Your Organization / College]