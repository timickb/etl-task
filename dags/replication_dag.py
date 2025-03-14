from datetime import datetime
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 1),
    "retries": 1,
    "retry_delay": 60,
}

with DAG(
    dag_id="replicate_user_sessions",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["example", "mongo", "postgres", "etl"]
) as dag:

    def extract_from_mongo(**context):
        mongo_hook = MongoHook(conn_id="mongo_default")
        collection = mongo_hook.get_collection(
            mongo_db="users",
            mongo_collection="UserSessions"
        )

        query = {}

        cursor = collection.find(query)
        documents = list(cursor)

        for doc in documents:
            doc["_id"] = str(doc["_id"])

        # Возвращаем данные, чтобы использовать в XCom
        return documents

    def transform_data(**context):
        ti = context['ti']
        documents = ti.xcom_pull(task_ids='extract_from_mongo')

        transformed = []
        for doc in documents:
            # Добавим поле с количественным признаком (количество посещённых страниц)
            pages_count = len(doc.get("pages_visited", []))
            
            # Превратим поле device в единый формат (прописные буквы)
            device_str = str(doc.get("device", "")).lower()

            transformed_doc = {
                "session_id": doc["session_id"],
                "user_id": doc["user_id"],
                "start_time": doc["start_time"],
                "end_time": doc["end_time"],
                "pages_visited": doc["pages_visited"],
                "pages_visited_count": pages_count,
                "device": device_str,
                "actions": doc["actions"],
            }
            transformed.append(transformed_doc)

        return transformed

    def load_to_postgres(**context):
        ti = context['ti']
        transformed_docs = ti.xcom_pull(task_ids='transform_data')

        pg_hook = PostgresHook(postgres_conn_id="postgres_default")


        insert_sql = """
            INSERT INTO user_sessions (
                session_id,
                user_id,
                start_time,
                end_time,
                pages_visited,
                device,
                actions,
                pages_visited_count
            )
            VALUES (%(session_id)s, %(user_id)s, %(start_time)s, %(end_time)s,
                    %(pages_visited)s, %(device)s, %(actions)s, %(pages_visited_count)s)
            ON CONFLICT (session_id)
            DO UPDATE SET
                user_id = EXCLUDED.user_id,
                start_time = EXCLUDED.start_time,
                end_time = EXCLUDED.end_time,
                pages_visited = EXCLUDED.pages_visited,
                device = EXCLUDED.device,
                actions = EXCLUDED.actions,
                pages_visited_count = EXCLUDED.pages_visited_count;
        """

        with pg_hook.get_conn() as conn:
            with conn.cursor() as cur:
                for doc in transformed_docs:
                    cur.execute(insert_sql, doc)

        inserted_count = len(transformed_docs)
        print(f"[OK] Inserted/Updated {inserted_count} rows into Postgres user_sessions table.")

    t1 = PythonOperator(
        task_id="extract_from_mongo",
        python_callable=extract_from_mongo
    )

    t2 = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    t3 = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    t1 >> t2 >> t3