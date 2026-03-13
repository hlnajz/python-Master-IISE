# Advanced Python Programming: Smart Embedded Control Platform
**Academic Year:** 2025/2026  
**Track:** Excellence Master’s Degree – IISE  
**Architect:** Hamza Labbaalli  
**Professor:** Pr. OUKDACH  

---

## 📌 Project Overview
This repository contains the complete set of exercises for the **Advanced Python Programming** module. The project is divided into two main sections: 

1.  **Fundamental OOP & Logic (Part 1):** Implementation of core Python concepts including `*args`, `**kwargs`, decorators, inheritance, and polymorphism.
2.  **Smart Embedded Control Platform (Part 2):** A high-level software architecture designed to manage modular embedded services (Sensors, Actuators, Communication) using advanced Design Patterns.

## 🚀 Key Features
- **Modular HAL (Hardware Abstraction Layer):** Easily plug in new hardware without modifying core logic.
- **Singleton System Monitoring:** Centralized logging to manage system-wide events and resource usage.
- **Real-time Performance Tracking:** A custom decorator used to measure hardware execution latency in milliseconds.
- **Dynamic Registry:** Uses Python Metaclasses to automatically register hardware modules at runtime.
- **Interactive Dashboard:** A Streamlit-based UI to visualize hardware tasks and execution timing.

---

## 📁 Repository Structure

### 🔹 Part 1: Core Fundamentals
| File | Exercise | Description |
| :--- | :--- | :--- |
| `ex1_basics.py` | 1 | Basic logic: even checks, list sums, and custom max logic. |
| `ex2_calc.py` | 2 | Variable arguments (`*args`) implementation for math operations. |
| `ex3_profile.py` | 3 | Dictionary manipulation and profile building (`**kwargs`). |
| `ex4_inventory.py`| 4 | Safe inventory management using dictionary methods. |
| `ex5_student.py` | 5 | Encapsulation and `@property` validation logic. |
| `ex6_bank.py` | 6 | Financial integrity and private attribute management. |
| `ex7_payroll.py` | 7 | Polymorphism in employee salary calculations. |
| `ex8_notifier.py` | 8 | Multiple inheritance and Mixin patterns. |

### 🔹 Part 2: Advanced Integration (The IISE Problematic)
| File | Title | Description |
| :--- | :--- | :--- |
| `app_iise.py` | **Smart Platform** | The final Streamlit application integrating the Strategy, Singleton, and Registry patterns. |

---

## 🛠️ Technical Implementation Details

### Design Patterns Used:
* **Singleton Pattern:** Implemented in `EmbeddedMonitor` to ensure a unified system log.
* **Strategy Pattern:** Used to define hardware behaviors (`SensorReading`, `ActuatorControl`) through a common interface.
* **Factory Pattern (via Metaclass):** Automates the creation of hardware objects without hardcoded `if/else` statements.
* **Decorator Pattern:** Used for cross-cutting concerns like measuring execution time.

---

## 💻 Installation & Usage

### Prerequisites
- Python 3.9+
- Streamlit
- Pandas

