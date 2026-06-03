# Skill: Python

## Core rules
- Follow PEP 8 — always
- Use type hints on all function signatures
- Use dataclasses or Pydantic models for data shapes — not plain dicts
- Prefer explicit over implicit
- Keep functions small and focused
- No mutable default arguments in function signatures

## Type hints
- Annotate all function parameters and return types
- Use Optional[T] for values that can be None
- Use Union sparingly — prefer narrower types
- Use TypedDict for dict shapes when Pydantic is not available
- Use Protocol for duck typing interfaces

## Error handling
- Use specific exception types — never catch bare Exception unless re-raising
- Create custom exception classes for domain errors
- Never silently swallow exceptions — log or re-raise
- Use context managers for resource management

## Async (FastAPI / async code)
- Use async/await consistently — do not mix sync and async
- Use async database drivers for async endpoints
- Never call blocking I/O in async functions — use run_in_executor
- Use asyncio.gather for parallel operations

## Imports
- Standard library first, third party second, local modules third
- No wildcard imports (from module import *)
- Use absolute imports

## Code organisation
- One module per concept
- Keep files under 300 lines
- Use __init__.py to control public API of packages
- Separate concerns — no business logic in route handlers

## Security
- Never use eval or exec on user input
- Validate all incoming data with Pydantic or similar
- Use parameterised queries — never string-format SQL
- Store secrets in environment variables — never in code
