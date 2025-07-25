# Use a slim Python image as the base
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Define the command to run the Streamlit application
CMD ["streamlit", "run", "ui/main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
