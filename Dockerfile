# Set the python base image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy the requirements.txt for dependencies
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Generate prisma client
RUN prisma generate --schema ./models/schema.prisma