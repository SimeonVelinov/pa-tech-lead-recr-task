# PA Tech Lead Task Streamlit app

A streamlit webapp that lets the user explore the world happiness report data.
The app has several pages that allow for visualization of the data in different ways.

---

## 📦 Clone the Repository
git clone https://github.com/SimeonVelinov/pa-tech-lead-recr-task

▶️ Run Locally

Make sure you have Python 3.8+ and pip installed.
1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Start the Streamlit app
streamlit run Main.py
The app will open in your browser at http://localhost:8501.

🐳 Run with Docker
1. Build the Docker image
docker build -t streamlit-app .

2. Run the Docker container
docker run -p 8501:8501 streamlit-app

Open http://localhost:8501 in your browser.

P.S. I am terrible at documentation. Sorry.