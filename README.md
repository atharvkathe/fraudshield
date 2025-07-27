# 🛡️ FraudShield - Smart Transaction Anomaly Detector

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-purple?style=for-the-badge&logo=pandas&logoColor=white)

A fully interactive web application that uses unsupervised machine learning to detect fraudulent financial transactions in real-time. This isn't just a script; it's a full-stack data science tool designed to be both powerful and user-friendly.

---

### 🚀 Live Demo

**https://atharvkathe-fraudshield-appmain-feyfdv.streamlit.app/**

---

### ✨ Key Features

* **Unsupervised Learning:** Utilizes the **Isolation Forest** algorithm to identify anomalies without needing pre-labeled fraud data. This allows it to detect new and emerging fraud patterns.
* **Interactive Dashboard:** A clean, modern UI built with Streamlit that provides a summary of the analysis, detailed transaction reports, and visual analytics.
* **Smart CSV Importer:** A robust data import tool that doesn't just let you upload a file—it intelligently auto-detects columns and lets you confirm the mapping, making the tool flexible for various real-world datasets.
* **Dual-Mode Analysis:** Seamlessly switch between a one-click **Demo Mode** using Faker-generated data and a **Power-User Mode** for uploading and analyzing custom CSV files.
* **Visual Analytics:** Features an interactive Plotly histogram showing the distribution of risk scores, allowing for dynamic threshold analysis.

---

### 🛠️ Tech Stack

* **Language:** Python
* **Data Manipulation:** Pandas
* **Machine Learning:** Scikit-learn (Isolation Forest)
* **Web Framework/UI:** Streamlit
* **Data Visualization:** Plotly Express
* **Synthetic Data:** Faker
* **Testing:** Pytest

### 🏁 Getting Started

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-link]
    cd fraudshield
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

### 🏃‍♂️ Usage

The project is designed to be run in a sequence:

1.  **Generate Raw Data:**
    ```bash
    python scripts/01_generate_data.py
    ```

2.  **Preprocess the Data:**
    ```bash
    python scripts/02_preprocess_data.py
    ```

3.  **Train the Model:**
    ```bash
    python scripts/03_train_model.py
    ```

4.  **Run the Streamlit Web App:**
    ```bash
    streamlit run app/main.py
    ```

---


### 🧠 The Journey & Key Learnings

* **Initial Vision:** The goal was to build a complete, end-to-end product, not just a model. This project demonstrates the full development lifecycle, from data generation to a live, interactive dashboard.

* **The Importer Challenge:** Early versions of the file uploader were brittle and crashed easily. This taught a critical lesson: a feature that *looks* flexible isn't the same as one that *is* robust. The final, smart importer that auto-detects columns was a breakthrough in building for real-world user needs.

* **Refactoring for Scale:** Moving functions from `main.py` into `utils.py` wasn't about fixing a bug, but implementing a professional software design pattern. Separating the UI from the logic makes the code cleaner, easier to maintain, and ready for future expansion.

* **The Power of Testing:** Writing automated tests with `pytest` provides a safety net for the project's foundation. It ensures the data generation script is reliable, which prevents the model from training on bad data and builds confidence to make future changes.

---

### 🔮 Future Enhancements

* **Explainable AI (XAI):** Integrate tools like SHAP to explain *why* a transaction was flagged, moving from a "what" to a "why."
* **Real-time Data Pipeline:** Connect the app to a streaming data source like Kafka to analyze transactions as they happen.
* **Feedback Loop:** Allow users to mark flagged transactions as "actual fraud" or "not fraud," and use this feedback to retrain and improve the model over time.

