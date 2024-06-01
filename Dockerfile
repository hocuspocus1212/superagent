# Use a base image that supports both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs18

# Set the working directory in the container
WORKDIR /app

# Copy the application source code to the container
COPY . /app

# Install Node.js and Python dependencies if they exist
RUN if [ -e package.json ]; then npm install; fi
RUN if [ -e requirements.txt ]; then pip install -r requirements.txt; fi

# Set the appropriate permissions and execute the script
RUN chmod 777 ./libs/superagent/replit.sh
CMD ["sh", "-c", "cd ./libs/superagent && ./replit.sh"]
