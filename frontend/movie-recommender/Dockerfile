ARG NODE_VERSION=24.12.0-alpine
ARG CADDY_VERSION=2.11.9-alpine

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the React.js application (outputs to /app/dist)
RUN npm run build

# Production image
FROM caddy:${CADDY_VERSION} AS runner

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=builder /app/dist /srv

EXPOSE 80 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
