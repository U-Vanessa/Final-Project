# Final-Project

## Design and Implementation of an Integrated ICT Asset and Support Management System

### Description
ASM (Asset & Support Management System) is a comprehensive, full-stack solution designed specifically for ICT departments and organizations to streamline asset tracking, support ticket management, and resource optimization. Built with FastAPI (Python) backend and React TypeScript frontend, it provides a robust, scalable platform for managing ICT infrastructure with real-time tracking and AI-powered assistance.

### Key Features
▫️ Smart Authentication - JWT-based secure login with role-based access

▫️ Asset Inventory - Complete hardware/software tracking

▫️ Support Ticket System - Efficient IT support workflow

▫️ AI Chat Assistant - AI-powered helpdesk and troubleshooting

▫️ Analytics Dashboard - Real-time metrics and reporting

▫️ Dark/Light Mode - User-friendly interface with theme switching

▫️ Responsive Design - Works on desktop, tablet, and mobile

### GitHub Repository
``` bash
Repository URL: https://github.com/U-Vanessa/Final-Project.git
```

### Repository Structure

asm-system/

├── backend/          # FastAPI Python backend

├── frontend/         # React TypeScript frontend

├── docs/             # Documentation

├── screenshots/      # Application screenshots

├── designs/          # Figma mockups & designs

└── README.md         # This file


### Environment Setup

Prerequisites
Python 3.9+ with pip

Node.js 18+ with npm/yarn

MongoDB 6.0+ (local or cloud instance)

### Git for version control

1. Clone Repository
```bash
git clone https://github.com/yourusername/asm-system.git
cd ASM
```
2. Backend Setup
```bash
# Navigate to backend directory
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
``` 
# Start FastAPI server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Verify Installation
```bash
Backend: Visit http://localhost:8000/docs for API documentation
```
```bash
Frontend: Visit http://localhost:3000 for the web application
```


### Designs & Mockups
Figma Designs
Figma Link: [https://www.figma.com/design/y5pAXgUPvQJJOG7cQNcODH/ASM?node-id=0-1&t=rRHX73v1o78dMkNM-1](https://www.figma.com/design/y5pAXgUPvQJJOG7cQNcODH/ASM?node-id=0-1&t=rRHX73v1o78dMkNM-1)

Design System
Primary Color: #3b82f6 (Blue)

Secondary Color: #8b5cf6 (Purple)

Font Family: Inter

Design Principles: Material Design 3

Application Screenshots
1. Login Interface
   <img width="1391" height="816" alt="{9B62683F-473B-4A95-8241-1E824C291848}" src="https://github.com/user-attachments/assets/0f8049f0-6eb0-4282-a67e-f9987192765a" />
Modern login interface with email/password authentication

3. Dashboard Overview
   <img width="1918" height="1143" alt="{A4BB5A2E-0ED5-41EE-9B7F-4732B0E2100C}" src="https://github.com/user-attachments/assets/4e838b0c-1a32-47ef-a149-a43a66ca76b4" />
Main dashboard with statistics, quick actions, and recent activity

4. Asset Management
https://screenshots/assets.png
Asset inventory with filtering and search capabilities

5. Voucher
   <img width="1904" height="1085" alt="{11FDFBF2-BB8E-4F45-A599-41C70A74D212}" src="https://github.com/user-attachments/assets/92fff924-45ae-4523-b5d3-ea9a8847033c" />
Voucher Support ticket management with status tracking

7. AI Chat Assistant
   <img width="1911" height="1084" alt="{CC054C33-0598-4116-A1A0-9485F4796192}" src="https://github.com/user-attachments/assets/98a844e9-2399-4f9f-83e1-96e3e9724194" />
AI-powered helpdesk for instant support


#### Architecture Diagram
<img width="22853" height="7885" alt="ASM- Architeture" src="https://github.com/user-attachments/assets/c029c3d6-9327-4e2f-a33b-a54c3c4d132a" />


### Deployment Plan

▫️Phase 1: Development Environment
✅ Complete - Local development setup

✅ Complete - Basic authentication system

✅ Complete - Dashboard and core components

Target: Internal testing and feature validation

▫️Phase 2: Staging Environment
✅ Backend deployed on Render Cloud Platform

✅ Automatic deployment via GitHub integration

✅ Environment variables managed securely on Render
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
✅ Frontend built using
```bash
npm run build
```
✅ Completed – System is live and accessible

▫️Phase 3: Production Environment (Future work)
▶️ Integration of cloud AI services (instead of local Ollama)
▶️ Migration to scalable cloud infrastructure (AWS/GCP)
▶️ Containerization using Docker

▫️Phase 4: Scaling & Optimization (Furure Work
▶️ Load balancing for high traffic
▶️ Database optimization
▶️ CDN integration for faster frontend delivery

### Video Demo 
- Part 1 [https://www.loom.com/share/b03521f0a2b54ddd963dafdcec2a6ed3 ](https://www.loom.com/share/b03521f0a2b54ddd963dafdcec2a6ed3)
- Part 2 [https://www.loom.com/share/7046ccd5dcfa461e9e5f712010ec8f04 ](https://www.loom.com/share/7046ccd5dcfa461e9e5f712010ec8f04)
- Part 3 [https://www.loom.com/share/38f21e7e13934ed790897c97213cb14b](https://www.loom.com/share/38f21e7e13934ed790897c97213cb14b)
- Final Project Part 1[https://www.loom.com/share/a728a819a20a400facca1eaef50e3cd0]([url](https://www.loom.com/share/a728a819a20a400facca1eaef50e3cd0))
- Final Project Part 2 [https://www.loom.com/share/62d8b745ff3d40118279d82e3fb59412]([url](https://www.loom.com/share/62d8b745ff3d40118279d82e3fb59412))

### Author
Vanessa UWONKUNDA 
