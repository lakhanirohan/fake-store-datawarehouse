CREATE OR REPLACE PROCEDURE FAKE_STORE.SILVER.GET_FACT_ORDERS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN

    INSERT OVERWRITE INTO FAKE_STORE.SILVER.FACT_ORDERS
    SELECT 
        src.$1:userId::number as user_id,
        src.$1:id::number as order_id,
        src.$1:date::timestamp::date as order_date,
        p.value:productId::number as product_id,
        p.value:quantity::number as quantity
    FROM FAKE_STORE.BRONZE.CARTS as src, LATERAL FLATTEN(input => src.$1:products) p;

    COMMIT;
    
    RETURN 'SUCCESS';

END;
$$;