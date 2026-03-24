-- Manufacturing Supply Chain Database Schema
-- Complex manufacturing domain with Bill of Materials (BOM) hierarchy
-- Features self-referencing Product table for multi-level assemblies

-- Create ENUM types
CREATE TYPE product_type_t AS ENUM ('FINISHED_GOOD', 'ASSEMBLY', 'COMPONENT');
CREATE TYPE status_t AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CLOSED');
CREATE TYPE priority_t AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT');
CREATE TYPE shipment_type_t AS ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL');
CREATE TYPE shipment_status_t AS ENUM ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED');
CREATE TYPE qc_type_t AS ENUM ('INCOMING', 'IN_PROCESS', 'FINAL');
CREATE TYPE qc_result_t AS ENUM ('PASS', 'FAIL', 'CONDITIONAL');
CREATE TYPE spec_type_t AS ENUM ('DIMENSIONAL', 'MATERIAL', 'PERFORMANCE');
CREATE TYPE qc_status_t AS ENUM ('PENDING', 'PASSED', 'FAILED', 'QUARANTINED');
CREATE TYPE yes_no_t AS ENUM ('Y', 'N');

-- PRODUCT table with self-reference for hierarchical assemblies
CREATE TABLE product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_type product_type_t NOT NULL DEFAULT 'FINISHED_GOOD',
    parent_product_id VARCHAR(20),
    base_cost DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    lead_time_days INT NOT NULL DEFAULT 0,
    is_active yes_no_t NOT NULL DEFAULT 'Y',
    CONSTRAINT fk_product_parent FOREIGN KEY (parent_product_id) REFERENCES product(product_id),
    CONSTRAINT chk_cost_nonnegative CHECK (base_cost >= 0),
    CONSTRAINT chk_lead_time_nonnegative CHECK (lead_time_days >= 0)
);

-- Index for hierarchical queries
CREATE INDEX idx_product_parent ON product(parent_product_id) WHERE parent_product_id IS NOT NULL;

-- COMPONENT table - atomic materials and parts
CREATE TABLE component (
    component_id VARCHAR(20) PRIMARY KEY,
    component_name VARCHAR(100) NOT NULL,
    component_category VARCHAR(50),
    unit_of_measure VARCHAR(10) NOT NULL DEFAULT 'EA',
    standard_cost DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    specification_id VARCHAR(20),
    CONSTRAINT chk_component_cost CHECK (standard_cost >= 0)
);

-- BOM (Bill of Materials) table - defines product composition
CREATE TABLE bom (
    bom_id VARCHAR(20) PRIMARY KEY,
    parent_product_id VARCHAR(20) NOT NULL,
    component_product_id VARCHAR(20) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL DEFAULT 1.000,
    unit_of_measure VARCHAR(10) NOT NULL DEFAULT 'EA',
    bom_level INT NOT NULL DEFAULT 0,
    is_optional yes_no_t NOT NULL DEFAULT 'N',
    CONSTRAINT fk_bom_parent FOREIGN KEY (parent_product_id) REFERENCES product(product_id),
    CONSTRAINT fk_bom_component FOREIGN KEY (component_product_id) REFERENCES product(product_id),
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_bom_level_nonnegative CHECK (bom_level >= 0),
    CONSTRAINT uq_bom_structure UNIQUE (parent_product_id, component_product_id)
);

-- Index for BOM explosion queries
CREATE INDEX idx_bom_parent ON bom(parent_product_id);
CREATE INDEX idx_bom_level ON bom(bom_level);

-- SUPPLIER table - external vendors
CREATE TABLE supplier (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    rating DECIMAL(3,2) NOT NULL DEFAULT 3.00,
    is_preferred yes_no_t NOT NULL DEFAULT 'N',
    CONSTRAINT chk_rating_range CHECK (rating >= 1.0 AND rating <= 5.0)
);

-- WAREHOUSE table - storage locations
CREATE TABLE warehouse (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    capacity INT NOT NULL DEFAULT 0,
    manager_id VARCHAR(20),
    CONSTRAINT chk_capacity_positive CHECK (capacity > 0)
);

-- INVENTORY table - stock levels
CREATE TABLE inventory (
    inventory_id VARCHAR(20) PRIMARY KEY,
    warehouse_id VARCHAR(20) NOT NULL,
    component_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity_on_hand DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    quantity_reserved DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    reorder_threshold DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    last_restock_date DATE,
    CONSTRAINT fk_inventory_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
    CONSTRAINT fk_inventory_component FOREIGN KEY (component_id) REFERENCES component(component_id),
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT chk_inventory_nonnegative CHECK (quantity_on_hand >= 0 AND quantity_reserved >= 0),
    CONSTRAINT chk_inventory_item EXCLUDE (component_id WITH =) WHERE (component_id IS NOT NULL AND product_id IS NOT NULL)
);

-- Index for inventory lookups
CREATE INDEX idx_inventory_component ON inventory(component_id) WHERE component_id IS NOT NULL;
CREATE INDEX idx_inventory_product ON inventory(product_id) WHERE product_id IS NOT NULL;
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);

-- WORK_ORDER table - production jobs
CREATE TABLE work_order (
    work_order_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    parent_work_order VARCHAR(20),
    quantity_ordered DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    quantity_completed DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status status_t NOT NULL DEFAULT 'PENDING',
    priority priority_t NOT NULL DEFAULT 'MEDIUM',
    planned_start_date DATE,
    planned_end_date DATE,
    warehouse_id VARCHAR(20),
    CONSTRAINT fk_work_order_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT fk_work_order_parent FOREIGN KEY (parent_work_order) REFERENCES work_order(work_order_id),
    CONSTRAINT fk_work_order_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
    CONSTRAINT chk_quantity_ordered_positive CHECK (quantity_ordered > 0),
    CONSTRAINT chk_quantity_completed_nonnegative CHECK (quantity_completed >= 0),
    CONSTRAINT chk_quantity_completed_not_exceed CHECK (quantity_completed <= quantity_ordered),
    CONSTRAINT chk_dates_consistent CHECK (planned_end_date IS NULL OR planned_start_date IS NULL OR planned_end_date >= planned_start_date)
);

-- Index for work order queries
CREATE INDEX idx_work_order_product ON work_order(product_id);
CREATE INDEX idx_work_order_parent ON work_order(parent_work_order) WHERE parent_work_order IS NOT NULL;
CREATE INDEX idx_work_order_status ON work_order(status);
CREATE INDEX idx_work_order_dates ON work_order(planned_start_date, planned_end_date);

-- SHIPMENT table - material transfers
CREATE TABLE shipment (
    shipment_id VARCHAR(20) PRIMARY KEY,
    shipment_type shipment_type_t NOT NULL,
    warehouse_id VARCHAR(20),
    supplier_id VARCHAR(20),
    customer_id VARCHAR(20),
    ship_date DATE NOT NULL,
    estimated_arrival DATE,
    actual_arrival DATE,
    status shipment_status_t NOT NULL DEFAULT 'PENDING',
    CONSTRAINT fk_shipment_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
    CONSTRAINT fk_shipment_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    CONSTRAINT chk_shipment_dates CHECK (actual_arrival IS NULL OR ship_date IS NULL OR actual_arrival >= ship_date),
    CONSTRAINT chk_supplier_inbound CHECK (shipment_type = 'INBOUND' OR supplier_id IS NULL)
);

-- Index for shipment tracking
CREATE INDEX idx_shipment_warehouse ON shipment(warehouse_id);
CREATE INDEX idx_shipment_supplier ON shipment(supplier_id) WHERE supplier_id IS NOT NULL;
CREATE INDEX idx_shipment_dates ON shipment(ship_date, estimated_arrival);
CREATE INDEX idx_shipment_status ON shipment(status);

-- QUALITY_CONTROL table - inspection records
CREATE TABLE quality_control (
    qc_id VARCHAR(20) PRIMARY KEY,
    batch_id VARCHAR(20),
    specification_id VARCHAR(20),
    qc_date DATE NOT NULL,
    qc_type qc_type_t NOT NULL,
    inspector_id VARCHAR(20),
    result qc_result_t NOT NULL,
    defect_count INT NOT NULL DEFAULT 0,
    notes TEXT,
    CONSTRAINT chk_defect_count_nonnegative CHECK (defect_count >= 0)
);

-- Index for QC queries
CREATE INDEX idx_qc_batch ON quality_control(batch_id) WHERE batch_id IS NOT NULL;
CREATE INDEX idx_qc_specification ON quality_control(specification_id) WHERE specification_id IS NOT NULL;
CREATE INDEX idx_qc_date ON quality_control(qc_date);
CREATE INDEX idx_qc_result ON quality_control(result);

-- SPECIFICATION table - technical requirements
CREATE TABLE specification (
    specification_id VARCHAR(20) PRIMARY KEY,
    specification_name VARCHAR(100) NOT NULL,
    version VARCHAR(10) NOT NULL,
    effective_date DATE NOT NULL,
    spec_type spec_type_t NOT NULL,
    critical_parameter VARCHAR(100),
    min_value DECIMAL(10,3),
    max_value DECIMAL(10,3),
    unit_of_measure VARCHAR(10),
    CONSTRAINT chk_min_max CHECK (max_value IS NULL OR min_value IS NULL OR max_value >= min_value)
);

-- Index for specification queries
CREATE INDEX idx_specification_type ON specification(spec_type);
CREATE INDEX idx_specification_effective ON specification(effective_date);

-- BATCH table - production lots
CREATE TABLE batch (
    batch_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    production_date DATE NOT NULL,
    quantity_produced DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    warehouse_id VARCHAR(20),
    expiry_date DATE,
    qc_status qc_status_t NOT NULL DEFAULT 'PENDING',
    CONSTRAINT fk_batch_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT fk_batch_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
    CONSTRAINT chk_quantity_produced_positive CHECK (quantity_produced > 0),
    CONSTRAINT chk_expiry_after_production CHECK (expiry_date IS NULL OR production_date IS NULL OR expiry_date >= production_date)
);

-- Index for batch queries
CREATE INDEX idx_batch_product ON batch(product_id);
CREATE INDEX idx_batch_date ON batch(production_date);
CREATE INDEX idx_batch_warehouse ON batch(warehouse_id);
CREATE INDEX idx_batch_qc_status ON batch(qc_status);

-- ROUTE table - manufacturing workflow steps
CREATE TABLE route (
    route_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    route_name VARCHAR(100) NOT NULL,
    sequence_number INT NOT NULL,
    operation_name VARCHAR(100) NOT NULL,
    work_center VARCHAR(50),
    cycle_time_minutes DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    setup_time_minutes DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_route_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT chk_sequence_positive CHECK (sequence_number > 0),
    CONSTRAINT chk_times_nonnegative CHECK (cycle_time_minutes >= 0 AND setup_time_minutes >= 0)
);

-- Index for route queries
CREATE INDEX idx_route_product ON route(product_id);
CREATE INDEX idx_route_sequence ON route(product_id, sequence_number);
CREATE UNIQUE INDEX uq_route_sequence ON route(product_id, sequence_number);

-- Component-Supplier relationship (many-to-many)
-- Links components to their approved suppliers
CREATE TABLE component_supplier (
    component_supplier_id VARCHAR(20) PRIMARY KEY,
    component_id VARCHAR(20) NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,
    is_preferred yes_no_t NOT NULL DEFAULT 'N',
    lead_time_days INT NOT NULL DEFAULT 0,
    unit_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_cs_component FOREIGN KEY (component_id) REFERENCES component(component_id),
    CONSTRAINT fk_cs_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    CONSTRAINT chk_cs_price_nonnegative CHECK (unit_price >= 0),
    CONSTRAINT uq_component_supplier UNIQUE (component_id, supplier_id)
);

CREATE INDEX idx_cs_component ON component_supplier(component_id);
CREATE INDEX idx_cs_supplier ON component_supplier(supplier_id);
