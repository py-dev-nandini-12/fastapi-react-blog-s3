# Full-Stack Blog Application with AWS S3 Storage

This is a full-stack blog application that allows users to upload images to an AWS S3 bucket, create blogs with titles and content, and view blogs with associated images.

## Backend Setup (FastAPI)

### Prerequisites
- Python 3.x installed
- AWS S3 bucket created with necessary permissions

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/blog-app.git

# Navigate to the backend directory
cd blog-app/backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Configuration
Set up AWS credentials by configuring AWS CLI or setting environment variables.
Run FastAPI Server
bash
Copy code
uvicorn main:app --reload
Frontend Setup (React)
Prerequisites
Node.js installed
Installation
bash
Copy code
# Navigate to the frontend directory
cd blog-app/frontend

# Install dependencies
npm install
Configuration
Update the .env file in the frontend directory with your FastAPI server URL.
Run React App
bash
Copy code
npm start
Usage
Access the React app at http://localhost:3000 in your browser.
Upload images in the designated section.
Create blogs with titles, content, and associate images.
View blogs with titles, content, and associated images.
