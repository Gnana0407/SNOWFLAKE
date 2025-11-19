-- Stored Procedure Example
-- This procedure updates customer information

CREATE OR REPLACE PROCEDURE MY_DATABASE.RAW_DATA.UPDATE_CUSTOMER(
    customer_id_param NUMBER,
    email_param VARCHAR,
    phone_param VARCHAR
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
    UPDATE MY_DATABASE.RAW_DATA.CUSTOMERS
    SET 
        EMAIL = :email_param,
        PHONE = :phone_param,
        UPDATED_DATE = CURRENT_TIMESTAMP()
    WHERE CUSTOMER_ID = :customer_id_param;
    
    RETURN 'Customer updated successfully';
END;
$$;
