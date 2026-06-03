# Skill: Java and SAP Commerce (Hybris)

## Java reading guide
- Entry points: look for @Controller, @RestController, @Facade annotations
- Business logic: look for @Service, Impl classes, ServiceLayer pattern
- Data access: look for DAO classes, FlexibleSearch queries, Repository pattern
- Data models: look for ItemType definitions in items.xml files
- Configuration: look for Spring XML configs, properties files, local.properties
- Integration points: look for @WebServiceEndpoint, client classes, outbound services

## SAP Commerce (Hybris) specific
- Items.xml: defines data model — read this first to understand entities and relations
- Facades: orchestrate business logic for presentation layer — entry point for API flows
- Converters and Populators: transform data between layers — follow the chain to understand data shape
- ServiceLayer: core business logic lives here
- Impex files: data setup and configuration — shows how system is configured
- Backoffice/HAC: admin configuration — look for backoffice config to understand business rules
- Extensions: modular architecture — each extension is a bounded context
- B2B Commerce: look for B2BUnit, B2BCustomer, approval workflows, cost centers
- B2C Commerce: look for CustomerModel, CartModel, OrderModel flows

## Reading an API flow in Hybris
When analysing an API endpoint follow this chain:
1. Controller → find the endpoint handler method
2. Facade → find the facade method called by controller
3. Service → find the service called by facade
4. DAO/FlexibleSearch → find how data is retrieved
5. Converter/Populator → find how data is transformed for response
6. items.xml → find the data model behind the flow

## B2B2C patterns
- B2B layer: organisations, units, budgets, approvals, purchase limits
- B2C layer: customer accounts, orders, cart, checkout
- Bridge: how B2B org context maps to B2C customer experience
- Marketplace integration: how third party sellers connect (Mirakl patterns)

## Mirakl integration patterns
- OR (Operator to Retailer) APIs: platform calling Mirakl
- Look for MiraklClient, MiraklApi classes
- Look for scheduled jobs that sync data with Mirakl
- Request/response mapping: find DTOs that map to Mirakl API contracts
- Error handling: find how Mirakl errors are handled and surfaced
- When reading Mirakl calls: note the API code (OR11, OR21, OR31 etc) — each has open documentation

## Reverse engineering checklist
When analysing any flow:
- What triggers this flow? (API call, scheduled job, event)
- What data comes in? (request model, parameters)
- What business rules are applied? (validations, transformations)
- What external systems are called? (Mirakl, payment, ERP)
- What data goes out? (response model)
- What is persisted? (which models are saved)
- What can go wrong? (error handling, fallbacks)

## Documentation notes
- Hybris code is verbose — focus on intent not implementation detail
- Spring DI means classes are wired at runtime — trace through interfaces to find implementations
- Many patterns are Hybris conventions — note when something is platform standard vs custom
- FlexibleSearch is SQL-like but object oriented — translate to plain English what data is fetched
