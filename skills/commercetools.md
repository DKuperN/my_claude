# Skill: Commercetools

## Platform overview
Commercetools is a headless, API-first commerce platform built on MACH principles:
Microservices, API-first, Cloud-native, Headless.
Everything is accessible via REST API or GraphQL.
No monolith — each capability is an independent service.

## Core concepts

### Project and Stores
- Project: top-level isolated environment
- Store: scoped view of the project — controls which products, prices, languages are visible
- Channel: represents a distribution channel or inventory location
- Use Stores for B2B2C: each brand (Nordstrom, Bloomingdale) can be a separate Store
- CustomerGroup: segments customers for pricing and access rules

### Product catalogue
- ProductType: defines the schema — attributes and their types
- Product: the master record with common attributes
- ProductVariant: specific sellable version (size, colour) — always at least one per Product
- Category: hierarchical catalogue organisation
- Custom Types + CustomFields: extend any entity without schema migration

### Pricing
- Prices live on ProductVariants — not on Products
- Price selection: channel, customerGroup, country, currency, date range
- Standalone Prices: prices managed separately from product (Import API friendly)
- Tiered pricing: supported natively via quantity-based price tiers

### Cart and Order flow
- Cart → Order is the core commerce flow
- LineItem: product in cart — references ProductVariant
- CustomLineItem: non-product item (service fee, gift wrap)
- CartDiscount: automatic discount applied to cart
- DiscountCode: code-triggered discount
- TaxCategory + TaxRate: flexible tax configuration per country/region
- Order states: Open → Confirmed → Complete → Cancelled
- OrderEdit: modify an order after creation without cancelling

### Customers
- Customer: registered user with addresses, CustomerGroup membership
- AnonymousCart → Customer merge on login
- B2B: use Associates, BusinessUnits for org hierarchy
- BusinessUnit: company or division in B2B context
- AssociateRole: permissions within a BusinessUnit

### Inventory
- InventoryEntry: stock per SKU per Channel
- ReservationMode: on order or on payment
- Supply Channel: warehouse or fulfilment location

### Extensibility
- Custom Types: add custom fields to any CT resource
- Extensions: serverless hooks — called synchronously on API requests
- Subscriptions: async event notifications (SNS, SQS, EventBridge)
- API Extensions: intercept and modify requests before they are processed

### Import and migration
- Import API: bulk import of products, prices, orders, customers
- Import Containers: named queues for import jobs
- Import is async — use import summaries to track status
- Recommended for Hybris migration: Import API for catalogue, prices, customer data

## B2B2C patterns in Commercetools

### Multi-brand setup
- One CT Project per environment (dev, staging, prod)
- Separate Stores per brand — controls product visibility and pricing
- Separate Channels per brand for inventory and pricing
- CustomerGroups per brand for customer segmentation
- Use Store-scoped API calls — never mix brand contexts in one call

### B2B specifics
- BusinessUnit hierarchy: Company → Division → Department
- Associates: users with roles within a BusinessUnit
- Approval Rules: order approval workflows (requires B2B feature)
- Purchase Limits: budget controls per BusinessUnit
- Quote management: request, negotiate, convert to order

### B2C specifics
- Standard Customer accounts with address book
- Anonymous cart support
- Promotions via CartDiscounts and DiscountCodes
- Wishlist via ShoppingList resource

### Marketplace integration (Mirakl + CT)
- Orders originating from Mirakl sync to CT as Orders with custom fields
- Use CustomType on Order to store Mirakl-specific fields (marketplace order ID, seller info)
- Cancellations: trigger Mirakl API calls via CT Subscription on Order state change
- Fulfilment: sync Mirakl shipment events back to CT Order via API Extension or Lambda

## Migration from Hybris to Commercetools

### Data mapping
- Hybris ProductModel → CT Product + ProductVariant
- Hybris CatalogVersion → CT Store + Channel
- Hybris PriceRow → CT Price on ProductVariant or StandalonePrice
- Hybris CustomerModel → CT Customer
- Hybris B2BUnitModel → CT BusinessUnit
- Hybris OrderModel → CT Order
- Hybris AbstractOrderEntryModel → CT LineItem
- Hybris FlexibleSearch → CT GraphQL or Query Predicates

### Migration approach
- Migrate catalogue first — Products, Categories, ProductTypes
- Migrate prices second — after catalogue is stable
- Migrate customers — before go-live
- Orders: historical orders stay in Hybris, new orders go to CT
- Use Import API for bulk data — not REST API one by one
- Run parallel for validation period — both systems live

### Common Hybris to CT pitfalls
- Hybris variants are flatter — CT requires explicit ProductType schema design upfront
- Hybris price rows are flexible — CT price selection rules are more structured
- Hybris promotions are rule-based engine — CT discounts are simpler, complex promos need Extensions
- Hybris B2B approval is built-in — CT B2B approval requires configuration
- Hybris FlexibleSearch has no CT equivalent — use Query Predicates or GraphQL

## API best practices
- Always use Store-scoped endpoints for storefront operations
- Use GraphQL for read-heavy operations — fetch only needed fields
- Use REST for write operations
- Paginate large result sets — use query offset or search after
- Use expand parameter carefully — it increases response size
- Cache product catalogue — CT rate limits apply per project
- Use Subscriptions for async workflows — never poll for state changes
- Version conflicts: CT uses optimistic locking — always send current version number
