# PDF Q&A Application

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/H57aves14co/0.jpg)](https://youtu.be/H57aves14co)

Click the image above to watch the demo video on YouTube.


## 🚀 Built for AiPlanet Internship
This project was built as an **internship project for AiPlanet**.

## 📌 Project Overview
The **PDF Q&A Application** is a **Full-Stack project** that allows users to **upload PDFs** and **ask questions** about their contents. It extracts text from the PDFs, builds an **AI-powered knowledge base**, and retrieves **relevant answers** using **FastAPI** (Backend) and **React + Vite** (Frontend).

## 🚀 Features
✅ Upload PDFs via a **user-friendly interface**  
✅ Extract and process text from uploaded PDFs  
✅ AI-powered **question-answering** based on document contents  
✅ Uses **FastAPI** for backend & **React (Vite)** for frontend  
✅ Local **vector database indexing** for fast search & retrieval  
✅ Fully **responsive** and **beginner-friendly setup**  
✅ Requires a **Hugging Face API Key** for AI-powered features  

## 🛠️ Tech Stack
### **Backend (FastAPI)**
- FastAPI (Python)
- LlamaIndex (for document indexing)
- SQLite / PostgreSQL (Database)
- PyMuPDF (Text Extraction)
- CORS Middleware (for frontend-backend communication)

### **Frontend (React + Vite)**
- React.js (UI framework)
- Vite (Frontend build tool)
- Axios (API requests)
- Tailwind CSS (Styling)
- Lucide React (Icons)

---

## 🖥️ Setup Guide (Local Installation)
Follow these steps to set up the project on your laptop:

### **1️⃣ Clone the Repository**
```bash
# Clone the project
git clone https://github.com/your-username/pdf-qa-app.git
cd pdf-qa-app
```

### **2️⃣ Backend Setup (FastAPI)**
```bash
cd backend  # Navigate to backend folder

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python main.py or uvicorn main:app --reload or python -m uvicorn main:app --reload   ( ANY ONE!)
```
🔹 The FastAPI server will start at **`http://127.0.0.1:8000`**

### **3️⃣ Add Hugging Face API Key**
This project requires a **Hugging Face API Key** for AI-powered question-answering. 

#### **How to Generate a Hugging Face API Key:**
1. Go to [Hugging Face](https://huggingface.co/)
2. Click on **Sign Up** (or log in if you already have an account).
3. Once logged in, go to **Settings** → **Access Tokens**.
4. Click **New Token**, set the role to **Write**, and generate the token.
5. Copy the generated token.

#### **How to Add the API Key to Your Project:**
1. Create a `.env` file inside the `backend` folder.
2. Add the following line in your `.env` file:
   ```
   HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_key_here
   ```
3. Restart the FastAPI server after adding the API key.

### **4️⃣ Frontend Setup (React + Vite)**
```bash
cd frontend  # Navigate to frontend folder

# Install dependencies
npm install

# Start the React app
npm run dev
```
🔹 The React app will be available at **`http://localhost:5173`**

---

## 📝 Usage Instructions
### **1️⃣ Upload a PDF**
- Go to the web app.
- Click the **Upload PDF** button.
- Select a **PDF file** from your device.
- The file will be uploaded and processed.

### **2️⃣ Ask Questions**
- Type your question in the chatbox.
- Click **Send** to get an AI-generated answer.
- The system will analyze the document and provide relevant responses.

---

## 🛠️ Troubleshooting
🔹 If **backend is not working**, check for missing dependencies and ensure FastAPI is running.  
🔹 If **frontend is not connecting**, verify that **CORS is enabled** in FastAPI.  
🔹 If you see **Indexing errors**, ensure PDFs are uploaded to the correct folder.  
🔹 If AI responses are not working, check if the **Hugging Face API Key** is correctly set in the `.env` file.

---

## 🤝 Contributing
We welcome contributions! 🎉

1. **Fork the repo** & create a new branch
2. **Make improvements** (Fix bugs, add features, improve UI)
3. **Submit a Pull Request**

---

## 📜 License
This project is **open-source** and licensed under the **MIT License**.

📩 Feel free to reach out if you have any questions! 🚀  
📧 Contact: **akhtersharique75@gmail.com**

