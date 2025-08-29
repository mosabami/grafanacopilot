# Multi-stage Dockerfile for building and serving the Vite React frontend

# Build stage
FROM node:18-alpine AS build
WORKDIR /app

# Allow passing VITE_ prefixed environment variables at build time
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Copy package files and install dependencies (use npm ci if lockfile present)
COPY package*.json ./
RUN if [ -f package-lock.json ]; then npm ci --silent; else npm install --silent; fi

# Copy source and build
COPY . .
RUN npm run build

# Production stage - serve the build via nginx
FROM nginx:stable-alpine AS production

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy build output
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a minimal nginx config that supports SPA fallback to index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]