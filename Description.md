# 🕹️ CTF Challenge Simulator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A lightweight and interactive **CTF (Capture The Flag) Challenge Simulator** built with **Python Flask**.  
It’s designed to teach and test cybersecurity concepts like **cryptography, steganography, and forensics** in a safe, local environment.  

---

## 📖 Abstract
This project implements a lightweight and interactive CTF Challenge Simulator designed to teach and test cybersecurity concepts in a controlled, local environment. Built using Python Flask, the application offers command-based interaction through a browser, enabling users to solve common CTF tasks like cryptography, steganography, and forensics.  

It features:
- Built-in **rate-limiting**  
- **IP-based abuse detection**  
- **Event logging**  

The system is tailored for students, hobbyists, or cyber clubs to practice ethical hacking in a safe and educational way.

---

## 🚀 Project Overview
The simulator provides a **command-driven CTF environment** accessible via a web browser.  
Users can:
- Learn and solve CTF challenges  
- Understand how common vulnerabilities and encoding techniques work  

---

## 🛠 Tech Stack
- **Backend:** Python + Flask  
- **Frontend:** HTML + TailwindCSS  
- **Data Handling:** Python dictionaries for storing challenges  

---

## ✨ Key Features
- **Multiple CTF Challenges** – cryptography, steganography, forensics  
- **Command Interface** – Commands like:  
  - `HELP` → list commands  
  - `LIST` → show challenges  
  - `CHALLENGE <name>` → open challenge  
  - `SOLVE` → submit solution  
- **IP Rate Limiting** – Only 5 requests/minute/IP  
- **Abuse Detection** – Blocks users after 3 invalid/suspicious commands  
- **Logging** – All activity stored in `ctf_web.log`  

---

## 🖥️ Why Local Server?
Running locally ensures:
- ✅ No internet or hosting dependency  
- ✅ Zero cost & full control  
- ✅ Easy customization of challenges  

---

## 📸 Output Demo
- **Welcome Screen**  
- **Challenge Screen**  
- **Solve Attempt View**  
- **Temporary Block Message**  
![Uploading 1.JPG…]()
Welcome Screen
![2](https://github.com/user-attachments/assets/3a35478a-0a17-4941-93be-d1d237a75801)
Command Line
![3](https://github.com/user-attachments/assets/9eb59f5b-2c88-4fe9-93e4-a120ca0fed25)
HElP
![4](https://github.com/user-attachments/assets/d3ec8cf3-2b40-434a-b7a8-6aa0da4a6ca4)
CHALLENGE LIST
![5](https://github.com/user-attachments/assets/cf97cb57-1906-461b-ba4f-a0a662efa085)
FLAG SUBMISSION
---

## 🏁 Conclusion
This project provides a **lightweight, safe, and efficient** simulator for learning cybersecurity.  
It’s ideal for:
- Students  
- Cybersecurity clubs  
- Beginners exploring ethical hacking concepts  

---

## ⚡ Getting Started

```bash
# Clone repo
git clone https://github.com/your-username/ctf-simulator.git
cd ctf-simulator

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Visit 👉 `http://localhost:5000`

---

## 📦 Requirements

```
Flask==2.3.2
Flask-Limiter==3.5.0
```

*(You can auto-generate an exact list by running `pip freeze > requirements.txt` after setup)*

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---
