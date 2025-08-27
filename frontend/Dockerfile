# ========================================
# Dependencies Stage - Install packages
# ========================================
FROM node:24.6-alpine AS deps

# Install system dependencies for node-gyp
RUN apk add --no-cache libc6-compat

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies using lock file
RUN npm ci --omit=dev --no-audit --no-fund && \
    npm cache clean --force

# ========================================
# Builder Stage - Build the application
# ========================================
FROM node:24.6-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files for full install
COPY package*.json ./

# Install ALL dependencies for building (including dev dependencies)
RUN npm ci --no-audit --no-fund && \
    npm cache clean --force

# Copy source code
COPY . .

# Set build environment
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build the application
RUN npm run build

# ========================================
# Development Stage - Development runtime with hot reload
# ========================================
FROM node:24.6-alpine AS development

# Install system dependencies
RUN apk add --no-cache libc6-compat

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies)
RUN npm ci --no-audit --no-fund

# Set development environment
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]

# ========================================
# Runner Stage - Production runtime
# ========================================
FROM node:24.6-alpine AS runner

# Metadata
LABEL maintainer="Alex Poloz <alexypoloz@gmail.com>"
LABEL description="Next.js frontend application"
LABEL version="1.0.0"

# Install runtime dependencies
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Set working directory
WORKDIR /app

# Set environment variables
ENV NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

# Copy production dependencies only
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules

# Copy built application from builder
COPY --from=builder --chown=nextjs:nodejs /app/next.config.ts ./
COPY --from=builder --chown=nextjs:nodejs /app/postcss.config.mjs ./
COPY --from=builder --chown=nextjs:nodejs /app/components.json ./
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
