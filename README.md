# 🚀 PipDynamics

AI-Powered Forex Signal Engine with Real-Time Dashboard

---

## 📌 Overview

PipDynamics is a full-stack AI trading system that generates BUY / SELL / WAIT signals using a trained Random Forest model and real-time MT5 data.

It includes:

- 📊 React Dashboard  
- ⚡ FastAPI Backend  
- 🤖 Machine Learning Signal Engine  
- 📈 ATR-based Risk Management  
- 🔁 Live Price Polling  
- 🎯 Probability-Based Decision Logic  

---

## 🧠 Tech Stack

### Frontend
- React
- Custom Chart Component
- Context API

### Backend
- FastAPI
- Python
- RandomForest ML Model
- MetaTrader 5 Live Data Integration

---

## 📊 Features

- Dynamic BUY / SELL / WAIT signals  
- Confidence scoring (0–100%)  
- Strength classification (Weak / Moderate / Strong)  
- ATR-based Stop Loss & Take Profit  
- Risk Reward Ratio calculation  
- Live market updates  

---

## ⚙️ Installation

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload