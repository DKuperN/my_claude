# Skill: TypeScript

## Type system rules
- Always use strict mode — no exceptions
- No implicit any — every variable and parameter must have explicit type
- Use interface for object shapes that describe data
- Use type for unions, intersections, and aliases
- Never use any — use unknown and narrow with type guards
- Use never for exhaustive checks in switch statements
- Prefer readonly for data that should not be mutated
- Use enums only for stable constants — prefer union types for flexibility
- Generic types must have meaningful names — not just T, use TEntity, TResponse
- Return types must be explicit on all public functions

## Null and undefined
- Enable strictNullChecks — always
- Use optional chaining (?.) instead of manual null checks
- Use nullish coalescing (??) instead of || for defaults
- Never return null and undefined from the same function — pick one
- Use NonNullable<T> when you know value exists

## Error handling
- Create typed error classes — never throw plain strings
- Use Result pattern or typed errors for expected failure cases
- Always type catch blocks — catch (error: unknown)
- Narrow error type before accessing properties
- Never swallow errors silently

## Async
- Always await promises — never fire and forget unless explicitly intentional
- Use Promise.all for parallel independent operations
- Use Promise.allSettled when some failures are acceptable
- Never mix async/await with .then() in the same function
- Always handle rejection — unhandled promise rejections are bugs

## Modules and imports
- Use named exports — avoid default exports except for React components
- Group imports: external packages first, then internal modules
- Use path aliases instead of deep relative imports (../../..)
- No circular dependencies

## Code organisation
- One concept per file
- Keep files under 200 lines
- Types and interfaces in separate files or co-located with their module
- No barrel files (index.ts re-exporting everything) in large modules — they hide dependencies
