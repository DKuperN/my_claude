# Skill: JavaScript

## Core rules
- Use const by default — let only when reassignment is needed — never var
- Use strict equality (===) always
- No implicit type coercion — be explicit
- Destructure objects and arrays where it improves readability
- Use optional chaining and nullish coalescing
- No magic numbers or strings — use named constants

## Functions
- Prefer arrow functions for callbacks and short functions
- Use regular functions for methods and constructors
- Keep functions small — one responsibility
- Avoid more than 3 parameters — use options object instead
- Pure functions where possible — same input always same output

## Async
- Use async/await — avoid raw promise chains
- Always handle errors with try/catch in async functions
- Use Promise.all for parallel operations
- Never use callbacks for new code unless required by external API

## Objects and arrays
- Use spread operator for shallow copies
- Use Array methods (map, filter, reduce) over loops where readable
- Do not mutate function arguments
- Use Object.freeze for constants that are objects

## Error handling
- Always throw Error objects — never strings
- Include context in error messages
- Handle errors at the right level — not too early, not too late

## Modules
- Use ES modules (import/export) — not CommonJS unless required
- Named exports preferred over default exports
- No circular dependencies
