# Skill: Software Architecture

## Core principles
- Separation of concerns — each module has one clear responsibility
- High cohesion, low coupling — related things together, unrelated things apart
- Depend on abstractions — not concrete implementations
- Explicit over implicit — make dependencies and data flow visible
- Simple over clever — complexity is a liability

## Microservices
- Each service owns its data — no shared databases between services
- Services communicate via APIs or events — not direct database access
- Define clear service boundaries around business capabilities
- Services should be independently deployable
- Design for failure — any service can go down at any time
- Use circuit breakers for calls to external services
- Avoid distributed monolith — if services must always deploy together they are not microservices

## API design
- REST: use nouns for resources, HTTP methods for actions
- Use consistent error response format across all services
- Version APIs from the start — /api/v1/
- Backwards compatible changes only in existing versions
- Document breaking changes — never silently change contracts
- Validate requests at the API boundary — not deep in business logic
- Return appropriate HTTP status codes — not always 200

## Event driven patterns
- Events describe what happened — past tense, immutable
- Producers do not know about consumers
- Design events for consumers — include enough data to avoid callbacks
- Use event schema registry for shared event contracts
- Handle duplicate events — consumers must be idempotent
- Dead letter queues for failed event processing

## Data patterns
- Repository pattern for data access — business logic does not know about database
- Never leak database models into API responses — use DTOs
- Validate data at boundaries — not in the middle of business logic
- Keep business logic pure — no I/O in domain logic
- Use transactions for operations that must succeed or fail together

## Common patterns
- Service layer — orchestrates use cases, calls repositories, no HTTP knowledge
- Repository — data access only, no business logic
- DTO (Data Transfer Object) — shapes data for transport, not for business logic
- Factory — creates complex objects, hides construction details
- Strategy — interchangeable algorithms behind common interface

## Antipatterns to avoid
- God object — one class that knows and does everything
- Tight coupling — changing one module requires changing many others
- Anemic domain model — objects with data but no behaviour
- Premature optimisation — optimise after profiling, not before
- Cargo cult patterns — using patterns without understanding why
- Distributed monolith — microservices that cannot deploy independently
- Shared database — multiple services reading and writing the same tables
- Chatty services — too many small API calls instead of one meaningful call

## Refactoring guidance
- Refactor when adding a feature is harder than it should be
- Refactor in small steps — one concept at a time
- Never refactor and add features in the same commit
- Keep tests green throughout refactoring
- Stop when code is good enough — perfect is the enemy of done
- Document why a pattern was chosen — not just what it does
