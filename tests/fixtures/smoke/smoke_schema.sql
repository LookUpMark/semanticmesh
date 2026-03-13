-- Smoke test DDL: minimal two-table schema
-- Purpose: verify pipeline end-to-end with the smallest possible input

CREATE TABLE CUST_MASTER (
    CUST_ID    INT          NOT NULL PRIMARY KEY,
    FULL_NAME  VARCHAR(120) NOT NULL,
    EMAIL      VARCHAR(200) NOT NULL UNIQUE,
    REGION_CODE CHAR(3)
);

CREATE TABLE SALES_ORD (
    ORD_ID    INT            NOT NULL PRIMARY KEY,
    CUST_ID   INT            NOT NULL REFERENCES CUST_MASTER(CUST_ID),
    ORD_DATE  DATE           NOT NULL,
    TOTAL_AMT DECIMAL(12,2)  NOT NULL DEFAULT 0,
    STATUS    VARCHAR(20)    NOT NULL DEFAULT 'PENDING'
);
