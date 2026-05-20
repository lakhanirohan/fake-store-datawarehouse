CREATE OR REPLACE PROCEDURE FAKE_STORE.SILVER.GET_DIM_USERS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN

    INSERT OVERWRITE INTO FAKE_STORE.SILVER.DIM_USERS
    SELECT 
        $1:id::NUMBER AS USER_ID,
        UPPER($1:name.firstname) AS FIRST_NAME,
        UPPER($1:name.lastname) AS LAST_NAME,
        $1:email::VARCHAR AS EMAIL,
        REPLACE($1:phone, '-', '') AS PHONE,
        UPPER($1:address.number || ', ' || $1:address.street) AS ADDRESS,
        UPPER($1:address.city::varchar) AS CITY,
        SPLIT_PART($1:address.zipcode, '-', 1) AS ZIP,
        SPLIT_PART($1:address.zipcode, '-', 2) AS ZIP_PLUS_FOUR,
        $1:address.geolocation.lat::varchar as LATITUDE,
        $1:address.geolocation.long::varchar as LONGITDE,
    FROM FAKE_STORE.BRONZE.USERS;

    COMMIT;
    
    RETURN 'SUCCESS';

END;
$$;