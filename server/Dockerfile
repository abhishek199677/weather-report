FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
COPY server/package.json ./server/
RUN npm ci --workspace=server
COPY server/ ./server/
RUN npm run build -w server

FROM node:22-alpine AS runner
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY package.json package-lock.json ./
COPY server/package.json ./server/
RUN npm ci --workspace=server --omit=dev
COPY --from=builder /app/server/dist/ ./server/dist/
USER app
EXPOSE 3001
ENV NODE_ENV=production
CMD ["node", "server/dist/index.js"]
