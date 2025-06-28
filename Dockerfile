# Use an official Python runtime as base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Optionally define environment variables (these get overridden by Hugging Face Secrets)
ENV GROQ_API_KEY=${GROQ_API_KEY}
ENV USER_AGENT=${USER_AGENT}
ENV TAVILY_API_KEY=${TAVILY_API_KEY}
ENV ASTRA_DB_APPLICATION_TOKEN=${ASTRA_DB_APPLICATION_TOKEN}
ENV ASTRA_DB_ID=${ASTRA_DB_ID}
ENV ASTRA_DB_KEYSPACE=${ASTRA_DB_KEYSPACE} 

# Expose port Streamlit uses (8501)
EXPOSE 7860

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
