# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files from repo root context
COPY frontend/time-tracker/package*.json ./

# Install dependencies using lockfile
RUN npm ci

# Copy the rest of the application from repo root context
COPY frontend/time-tracker/. .

# Build the Next.js application
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy the standalone output
COPY --from=builder /app/.next/standalone ./
# Copy static files
COPY --from=builder /app/.next/static ./.next/static
# Copy public folder
COPY --from=builder /app/public ./public

# Expose the port Next.js runs on
EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Start the application
CMD ["node", "server.js"]
