FROM python:3.11.8-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

RUN npm install -g npm@10

COPY package*.json ./
RUN npm ci --omit=dev

COPY requirements-lock.txt ./

RUN python -m pip install --require-hashes -r requirements-lock.txt
COPY . .

CMD ["node", "index.js"]
