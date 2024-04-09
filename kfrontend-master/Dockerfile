# Use an official Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Install curl
RUN apk add --no-cache curl

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set the value of VITE_API_URL environment variable
ENV VITE_API_URL=http://backend:8000

# Expose the port on which the application will run
EXPOSE 3000

# Command to run the frontend server
CMD ["npm", "run", "dev"]

