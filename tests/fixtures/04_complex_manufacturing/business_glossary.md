# Manufacturing Business Glossary

This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, production workflows, and quality assurance processes.

## Product

A Product represents any manufactured item in the system, including finished goods ready for sale, sub-assemblies used in production, and individual components. Products are organized in a hierarchical structure where complex products can contain simpler products as parts. Each product has a unique identifier, name, type classification, base cost, and lead time for procurement or production. Products can be active or inactive based on current manufacturing requirements.

**Key Attributes:**
- Unique product identifier (20 characters)
- Product name and description
- Type classification: FINISHED_GOOD, ASSEMBLY, or COMPONENT
- Hierarchical relationship via parent_product_id
- Base cost and lead time information
- Active status flag

**Relationships:**
- A Product can have multiple child Products (via BOM hierarchy)
- A Product can reference a parent Product (for multi-level assemblies)
- Products are used in Work Orders for production
- Products appear in Shipments (outbound)
- Products are stored in Inventory records

## Component

A Component represents atomic raw materials or purchased parts that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers. Each component has a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements.

**Key Attributes:**
- Unique component identifier
- Component name and category classification
- Unit of measure (EA, KG, M, L, etc.)
- Standard cost for procurement
- Technical specification reference

**Relationships:**
- Components are supplied by multiple Suppliers (many-to-many)
- Components have Inventory records tracking stock levels
- Components may reference Specifications for quality requirements

## BOM (Bill of Materials)

The Bill of Materials (BOM) defines the composition of products by specifying which components and sub-assemblies are required to manufacture a parent product. Each BOM entry indicates a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure. BOM entries support recursive relationships to represent multi-level product assemblies.

**Key Attributes:**
- Unique BOM identifier
- Parent product reference (what is being built)
- Component product reference (what goes into it)
- Required quantity and unit of measure
- BOM level (depth in hierarchy)
- Optional component flag

**Relationships:**
- BOM connects Products to other Products (parent-child)
- Multiple BOM entries define a complete product structure
- BOM structure is used for material requirements planning
- BOM levels support hierarchical product explosions

## Supplier

A Supplier is an external vendor or company that provides raw materials, components, or finished goods to the manufacturing organization. Suppliers are evaluated based on performance ratings, preferred status for strategic partnerships, and maintain contact information for procurement operations. Suppliers are associated with components they can provide through approved supplier relationships.

**Key Attributes:**
- Unique supplier identifier
- Supplier name and contact details
- Contact email and phone number
- Performance rating (1.0 to 5.0 scale)
- Preferred supplier flag

**Relationships:**
- Suppliers provide multiple Components (many-to-many via component_supplier)
- Suppliers are linked to Inbound Shipments
- Suppliers have negotiated pricing and lead times per component

## Warehouse

A Warehouse represents a physical storage location where materials, components, and finished goods are stored. Warehouses have defined capacity limits, geographic location information, and are managed by designated managers. Warehouses serve as nodes in the supply chain network where inventory is held, shipments are received, and products are staged for production or distribution.

**Key Attributes:**
- Unique warehouse identifier
- Warehouse name and location
- Address, city, and state information
- Storage capacity limits
- Manager assignment

**Relationships:**
- Warehouses contain multiple Inventory records
- Warehouses receive and ship Shipments
- Warehouses are linked to Work Orders for production staging
- Warehouses store produced Batches

## Inventory

Inventory represents the actual stock levels of components and products stored in specific warehouses. Each inventory record tracks the quantity on hand, quantity reserved for pending orders, and reorder thresholds to trigger procurement. Inventory records support either components or products (but not both in the same record) and include timestamps for the last restock date.

**Key Attributes:**
- Unique inventory identifier
- Warehouse location reference
- Component OR Product reference (mutually exclusive)
- Quantity on hand (available stock)
- Quantity reserved (allocated but not shipped)
- Reorder threshold for replenishment
- Last restock date

**Relationships:**
- Inventory belongs to a Warehouse
- Inventory tracks either a Component or Product
- Inventory levels trigger procurement decisions
- Inventory is reserved for Work Orders and Shipments

## WorkOrder

A Work Order represents a production job or manufacturing run to produce a specified quantity of a product. Work Orders track planned versus completed quantities, status through the production lifecycle, priority levels, and planned dates. Work Orders can have hierarchical relationships where a parent work order may decompose into child work orders for different production stages or sub-assemblies.

**Key Attributes:**
- Unique work order identifier
- Product to be manufactured
- Parent work order reference (for decomposition)
- Quantity ordered and completed
- Status: PENDING, IN_PROGRESS, COMPLETED, CLOSED
- Priority: LOW, MEDIUM, HIGH, URGENT
- Planned start and end dates
- Warehouse location for production

**Relationships:**
- Work Orders produce Products
- Work Orders can have child Work Orders
- Work Orders are associated with Warehouses
- Work Orders consume Inventory (components)
- Work Orders produce output for Shipment

## Shipment

A Shipment represents the physical transfer of materials between warehouses, from suppliers to warehouses (inbound), or from warehouses to customers (outbound). Shipments track shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status. Internal shipments support material movement between warehouses.

**Key Attributes:**
- Unique shipment identifier
- Type: INBOUND, OUTBOUND, INTERNAL
- Warehouse destination or source
- Supplier reference (for inbound)
- Customer reference (for outbound)
- Ship date, estimated arrival, actual arrival
- Status: PENDING, SHIPPED, DELIVERED, CANCELLED

**Relationships:**
- Shipments connect Warehouses, Suppliers, and Customers
- Inbound Shipments reference Suppliers
- Shipments update Inventory levels
- Shipments fulfill Work Order outputs

## QualityControl

Quality Control (QC) represents inspection and testing activities performed on materials, in-process production, or finished goods. QC records track the type of inspection (incoming, in-process, final), inspection date, inspector, test results (pass, fail, conditional), defect counts, and notes. QC activities are associated with specific production batches and may reference technical specifications being tested.

**Key Attributes:**
- Unique QC identifier
- Batch reference (production lot being inspected)
- Specification reference (requirements being tested)
- QC date and inspector
- Type: INCOMING, IN_PROCESS, FINAL
- Result: PASS, FAIL, CONDITIONAL
- Defect count and notes

**Relationships:**
- QC inspections are performed on Batches
- QC tests against Specifications
- QC results determine Batch status
- QC failures trigger rework or scrap decisions

## Specification

A Specification defines technical requirements, standards, and acceptance criteria for materials or products. Specifications include version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure. Specifications ensure manufactured products meet engineering and customer requirements.

**Key Attributes:**
- Unique specification identifier
- Specification name and version
- Effective date
- Type: DIMENSIONAL, MATERIAL, PERFORMANCE
- Critical parameter name
- Minimum and maximum acceptable values
- Unit of measure for testing

**Relationships:**
- Specifications define requirements for Components
- Specifications are used in Quality Control inspections
- Specifications have version control for engineering changes

## Batch

A Batch represents a specific production lot or run of a product, tracking all units produced together in a single manufacturing cycle. Batches record the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status. Batches enable traceability for quality issues and inventory management for time-sensitive or lot-controlled products.

**Key Attributes:**
- Unique batch identifier
- Product reference
- Production date
- Quantity produced
- Warehouse storage location
- Expiry date (if applicable)
- QC status: PENDING, PASSED, FAILED, QUARANTINED

**Relationships:**
- Batches produce a specific Product
- Batches are stored in Warehouses
- Batches undergo Quality Control inspections
- Batches may have expiry dates for perishable goods
- Batches enable traceability and recall management

## Route

A Route defines the sequence of manufacturing operations or steps required to produce a product. Each route step specifies the operation name, work center where the operation is performed, cycle time for the operation, setup time required, and sequence number. Routes collectively define the manufacturing workflow and are used for production scheduling, capacity planning, and cost calculation.

**Key Attributes:**
- Unique route identifier
- Product reference
- Route name and sequence number
- Operation name and description
- Work center location
- Cycle time (per unit processing time)
- Setup time (fixed preparation time)

**Relationships:**
- Routes define manufacturing steps for Products
- Route steps are ordered by sequence_number
- Routes determine production capacity requirements
- Routes are used for scheduling Work Orders
