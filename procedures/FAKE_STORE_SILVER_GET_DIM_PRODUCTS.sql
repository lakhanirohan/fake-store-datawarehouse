CREATE OR REPLACE PROCEDURE FAKE_STORE.SILVER.GET_DIM_PRODUCTS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN

    INSERT OVERWRITE INTO FAKE_STORE.SILVER.DIM_PRODUCTS
    SELECT 
        src.$1:id::NUMBER(10,0) AS PRODUCT_ID,
        src.$1:title::varchar AS PRODUCT_NAME,
        src.$1:description::varchar as DESCRIPTION,
        src.$1:category::varchar as CATEGORY, 
        src.$1:price::NUMBER(10,2) AS PRICE,
        src.$1:rating.count::NUMBER(10,0) AS NUMBER_OF_RATINGS,
        src.$1:rating.rate::NUMBER(10,2) AS RATING
    FROM FAKE_STORE.BRONZE.PRODUCTS src;

    COMMIT;
    
    RETURN 'SUCCESS';

END;
$$;