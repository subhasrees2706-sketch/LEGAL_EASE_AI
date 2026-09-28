Start Project

cd C:\Users\vinup\Downloads\LegalEaseAI

Terminal 1, backend:

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

Terminal 2, frontend:

python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501

If python is unavailable, use:

C:\Users\vinup\AppData\Local\Python\pythoncore-3.14-64\python.exe -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501