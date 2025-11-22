# Python 3.10 image from Docker Hub.
# This gives us a clean Linux OS with Python 3.10 pre-installed.
FROM python:3.10-slim

# -setting up the Environment ---
# Set the "working directory" inside the container.
# All our commands will run from /app
WORKDIR /app

# --- Stage 3: Install Dependencies ---
# First, copy ONLY the requirements file into the container.
# We'll create this file in the next step.
COPY requirements.txt requirements.txt

# Now, install all the libraries. This is like running 'pip install'
# inside the container.
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy Our Project Files ---
# Copy all our project folders and files into the /app directory.
# The '.' means "copy everything from my current folder"
# The '/app/' is the destination (our WORKDIR)
COPY . /app/

# runtime command
# Tells the container what command to run when it starts.
# This is the same command we used to start our server.
# It will run: python app.py
CMD ["python", "app.py"]