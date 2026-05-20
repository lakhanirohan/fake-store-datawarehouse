import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.empty import EmptyOperator
from airflow.sdk import DAG
from requests.exceptions import ConnectionError, MissingSchema


with DAG(
    dag_id="fake_store",
    start_date=pendulum.today('UTC').add(days=-7),
    schedule=None,
):
    start_piepeline = EmptyOperator(
        task_id="start_pipeline"
    )

    fetch_orders_from_api = BashOperator(
        task_id="fetch_orders_from_api",
        bash_command="curl -o /tmp/carts.json 'https://fakestoreapi.com/carts'",
    )

    fetch_products_from_api = BashOperator(
        task_id="fetch_products_from_api",
        bash_command="curl -o /tmp/products.json 'https://fakestoreapi.com/products'",
    )

    fetch_users_from_api = BashOperator(
        task_id="fetch_users_from_api",
        bash_command="curl -o /tmp/users.json 'https://fakestoreapi.com/users'",
    )

    load_stage_orders = SQLExecuteQueryOperator(
        task_id="load_stage_orders",
        sql="PUT 'file:///tmp/carts.json' @fake_store.bronze.fake_store_stage;",
        conn_id="rohan_snow",
    )

    load_stage_products = SQLExecuteQueryOperator(
        task_id="load_stage_products",
        sql="PUT 'file:///tmp/products.json' @fake_store.bronze.fake_store_stage;",
        conn_id="rohan_snow",
    )

    load_stage_users = SQLExecuteQueryOperator(
        task_id="load_stage_users",
        sql="PUT 'file:///tmp/users.json' @fake_store.bronze.fake_store_stage;",
        conn_id="rohan_snow",
    )

    load_bronze_orders = SQLExecuteQueryOperator(
        task_id="load_bronze_orders",
        sql="CALL FAKE_STORE.BRONZE.GET_SRC_CARTS();",
        conn_id="rohan_snow",
    )

    load_bronze_products = SQLExecuteQueryOperator(
        task_id="load_bronze_products",
        sql="CALL FAKE_STORE.BRONZE.GET_SRC_PRODUCTS();",
        conn_id="rohan_snow",
    )

    load_bronze_users = SQLExecuteQueryOperator(
        task_id="load_bronze_users",
        sql="CALL FAKE_STORE.BRONZE.GET_SRC_USERS();",
        conn_id="rohan_snow",
    )

    load_silver_fact_orders = SQLExecuteQueryOperator(
        task_id="load_silver_fact_orders",
        sql="CALL FAKE_STORE.SILVER.GET_FACT_ORDERS();",
        conn_id="rohan_snow",
    )

    load_silver_dim_products = SQLExecuteQueryOperator(
        task_id="load_silver_dim_products",
        sql="CALL FAKE_STORE.SILVER.GET_DIM_PRODUCTS();",
        conn_id="rohan_snow",
    )

    load_silver_dim_users = SQLExecuteQueryOperator(
        task_id="load_silver_dim_users",
        sql="CALL FAKE_STORE.SILVER.GET_DIM_USERS();",
        conn_id="rohan_snow",
    )

    load_gold_customer_total_spend_report = SQLExecuteQueryOperator(
        task_id="load_gold_customer_total_spend_report",
        sql="CALL FAKE_STORE.GOLD.GET_CUSTOMER_TOTAL_SPEND_REPORT();",
        conn_id="rohan_snow",
    )

    pipeline_complete = EmptyOperator(
        task_id="pipeline_complete"
    )

start_piepeline >> [fetch_users_from_api, fetch_orders_from_api, fetch_products_from_api]
fetch_orders_from_api >> load_stage_orders >> load_bronze_orders >> load_silver_fact_orders
fetch_products_from_api >> load_stage_products >> load_bronze_products >> load_silver_dim_products
fetch_users_from_api >> load_stage_users >> load_bronze_users >> load_silver_dim_users
[load_silver_fact_orders, load_silver_dim_products, load_silver_dim_users] >> load_gold_customer_total_spend_report
load_gold_customer_total_spend_report >> pipeline_complete
