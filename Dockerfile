# Stage 1: Build
FROM node:lts-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve
FROM node:lts-alpine AS serve-stage
WORKDIR /app
COPY --from=build-stage /app/ ./
ENV NODE_ENV production
EXPOSE 8080
CMD ["npm", "run", "start"]
