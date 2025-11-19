-- Insert Sample Data
-- This script inserts sample data into the tables

-- Insert sample customers
INSERT INTO MY_DATABASE.RAW_DATA.CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com', '555-0101'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', '555-0102'),
    (3, 'Bob', 'Johnson', 'bob.johnson@example.com', '555-0103');

-- Insert sample orders
INSERT INTO MY_DATABASE.RAW_DATA.ORDERS (ORDER_ID, CUSTOMER_ID, ORDER_DATE, ORDER_AMOUNT, STATUS)
VALUES
    (101, 1, CURRENT_DATE(), 150.00, 'COMPLETED'),
    (102, 1, CURRENT_DATE(), 250.00, 'PENDING'),
    (103, 2, CURRENT_DATE(), 175.50, 'COMPLETED');

-- Insert sample products
INSERT INTO MY_DATABASE.RAW_DATA.PRODUCTS (PRODUCT_ID, PRODUCT_NAME, CATEGORY, PRICE)
VALUES
    (1001, 'Widget A', 'Electronics', 99.99),
    (1002, 'Widget B', 'Electronics', 149.99),
    (1003, 'Gadget C', 'Home', 75.00);
