# fake-store-datawarehouse
end-to-end data pipeline and transformation for fake store 

FakeStore API
     │
     ▼
Local Machine (Intermediate)
     │
     ▼
┌─────────────────────────────────────────┐
│              SNOWFLAKE                  │
│                                         │
│  🥉 BRONZE         (Raw JSON / VARIANT) │
│     ├── carts                           │
│     ├── products                        │
│     └── users                           │
│                                         │
│  🥈 SILVER         (Flattened & Modeled)│
│     ├── fact_orders                     │
│     ├── dim_products                    │
│     └── dim_users                       │
│                                         │
│  🥇 GOLD           (Business Reporting) │
│     └── spend_per_customer              │
└─────────────────────────────────────────┘
     ▲
     │
Apache Airflow (Orchestration)
