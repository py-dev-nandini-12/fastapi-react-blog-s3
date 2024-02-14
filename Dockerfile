# Stage 1: Build React App
FROM node:14 as react-build
WORKDIR /app
COPY frontend/blog /app
COPY frontend/blog/package.json /app/package.json

RUN npm install
RUN npm run build

# Stage 2: Build FastAPI Backend
FROM python:3.9 as backend-build
WORKDIR /app
COPY backend /app
RUN pip3 install -r requirements.txt



# Stage 3: Combine React and FastAPI

FROM python:3.9
WORKDIR /app
COPY --from=react-build /app/build /app/frontend/build
COPY --from=backend-build /app /app

# Install uvicorn and other dependencies
RUN pip3 install uvicorn
RUN pip3 install botocore
RUN pip3 install fastapi
RUN pip3 install sqlalchemy
RUN pip3 install boto3
RUN pip3 install psycopg2

# Expose the port on which the app will run
EXPOSE 8080
# Set the entrypoint

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
