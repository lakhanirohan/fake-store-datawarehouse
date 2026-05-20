CREATE OR REPLACE PROCEDURE FAKE_STORE.BRONZE.GET_SRC_CARTS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN

    INSERT OVERWRITE INTO FAKE_STORE.BRONZE.CARTS
        SELECT $1 as json_data 
        FROM @fake_store.bronze.fake_store_stage/carts.json.gz (file_format => fake_store.bronze.my_json_file_format);

    COMMIT;
    
    RETURN 'SUCCESS';

END;
$$;