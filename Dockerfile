FROM python:3.11.8-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

RUN npm install -g npm@10

COPY package*.json ./
RUN npm install --omit=dev

COPY requirements.txt ./

RUN python -m pip install --upgrade pip==24.0 \
 && pip install --no-cache-dir --requirement requirements.txt

COPY . .

CMD ["node", "index.js"]
