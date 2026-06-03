# Skill: Node.js

## Core principles
- Node.js is single-threaded — never block the event loop
- Use async I/O for all file, network, and database operations
- CPU-intensive work belongs in worker threads or separate services
- Keep memory usage predictable — avoid unbounded caches or queues

## HTTP and API
- Use proper HTTP status codes consistently
- Always set Content-Type headers explicitly
- Validate and sanitise all incoming request data
- Set request size limits — never accept unlimited payloads
- Use correlation IDs for request tracing across services
- Always handle timeouts on outbound HTTP calls

## Environment and configuration
- All configuration via environment variables — never hardcode
- Validate required environment variables at startup — fail fast if missing
- Use a config module to centralise env var access — not process.env scattered everywhere
- Never log environment variables or secrets

## Error handling
- Use a centralised error handler for Express/HTTP servers
- Distinguish operational errors (expected) from programmer errors (bugs)
- Operational errors: log and respond with appropriate HTTP status
- Programmer errors: log and restart the process
- Always listen to process uncaughtException and unhandledRejection

## Logging
- Use structured logging (JSON) — not plain console.log
- Include: timestamp, level, service name, correlation ID, message
- Log at appropriate levels: error, warn, info, debug
- Never log sensitive data — passwords, tokens, PII
- Log at service boundaries — incoming requests, outgoing calls, responses

## Performance
- Use streaming for large data — never load entire files into memory
- Pool database connections — never create per-request connections
- Cache expensive operations with appropriate TTL
- Use compression for HTTP responses

## Security
- Sanitise all user input before use
- Use helmet for HTTP security headers
- Rate limit public endpoints
- Never trust client-provided data for authorisation decisions
- Keep dependencies updated — audit regularly

## Process management
- Handle SIGTERM and SIGINT for graceful shutdown
- Close database connections and finish in-flight requests on shutdown
- Use health check endpoints for load balancers and orchestrators
