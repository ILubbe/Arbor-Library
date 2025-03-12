FROM node:22.13.1 AS build

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build --omit=dev

FROM nginx:1.24

COPY default-nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html