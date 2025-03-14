import random
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient

fake = Faker("en_US")

MONGO_URI = "mongodb://root:example@localhost:27017"
DATABASE_NAME = "users"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def generate_user_sessions(num_docs=50):
    """Генерация коллекции UserSessions."""
    data = []
    for _ in range(num_docs):
        start_time = fake.date_time_between(start_date="-30d", end_date="now")
        end_time = start_time + timedelta(minutes=random.randint(5, 180))

        document = {
            "session_id": fake.uuid4(),
            "user_id": random.randint(1, 1000),
            "start_time": start_time,
            "end_time": end_time,
            "pages_visited": [fake.uri_path() for _ in range(random.randint(1, 5))],
            "device": random.choice(["desktop", "mobile", "tablet"]),
            "actions": [fake.sentence() for _ in range(random.randint(1, 3))]
        }
        data.append(document)
    db.UserSessions.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into UserSessions")

def generate_product_price_history(num_docs=50):
    """Генерация коллекции ProductPriceHistory."""
    data = []
    for _ in range(num_docs):
        changes_count = random.randint(1, 5)
        price_changes = []
        current_time = datetime.now()
        for i in range(changes_count):
            change_time = current_time - timedelta(days=i * random.randint(1, 10))
            price_changes.append({
                "date": change_time,
                "price": round(random.uniform(10.0, 1000.0), 2)
            })

        document = {
            "product_id": fake.uuid4(),
            "price_changes": price_changes,
            "current_price": price_changes[0]["price"] if price_changes else 0,
            "currency": random.choice(["USD", "EUR", "RUB", "CNY"])
        }
        data.append(document)
    db.ProductPriceHistory.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into ProductPriceHistory")

def generate_event_logs(num_docs=50):
    """Генерация коллекции EventLogs."""
    data = []
    event_types = ["CLICK", "VIEW", "DOWNLOAD", "LOGIN", "LOGOUT", "ERROR"]
    for _ in range(num_docs):
        document = {
            "event_id": fake.uuid4(),
            "timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
            "event_type": random.choice(event_types),
            "details": fake.sentence()
        }
        data.append(document)
    db.EventLogs.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into EventLogs")

def generate_support_tickets(num_docs=50):
    """Генерация коллекции SupportTickets."""
    data = []
    statuses = ["open", "in_progress", "closed", "pending"]
    issue_types = ["billing", "technical", "account", "other"]
    for _ in range(num_docs):
        created_at = fake.date_time_between(start_date="-60d", end_date="now")
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        if updated_at > datetime.now():
            updated_at = datetime.now()
        document = {
            "ticket_id": fake.uuid4(),
            "user_id": random.randint(1, 1000),
            "status": random.choice(statuses),
            "issue_type": random.choice(issue_types),
            "messages": [fake.sentence() for _ in range(random.randint(1, 5))],
            "created_at": created_at,
            "updated_at": updated_at
        }
        data.append(document)
    db.SupportTickets.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into SupportTickets")

def generate_user_recommendations(num_docs=50):
    """Генерация коллекции UserRecommendations."""
    data = []
    for _ in range(num_docs):
        document = {
            "user_id": random.randint(1, 1000),
            "recommended_products": [fake.uuid4() for _ in range(random.randint(1, 3))],
            "last_updated": fake.date_time_between(start_date="-30d", end_date="now")
        }
        data.append(document)
    db.UserRecommendations.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into UserRecommendations")

def generate_moderation_queue(num_docs=50):
    """Генерация коллекции ModerationQueue."""
    data = []
    moderation_statuses = ["pending", "approved", "rejected"]
    for _ in range(num_docs):
        submitted_at = fake.date_time_between(start_date="-90d", end_date="now")
        document = {
            "review_id": fake.uuid4(),
            "user_id": random.randint(1, 1000),
            "product_id": random.randint(1, 500),
            "review_text": fake.text(max_nb_chars=100),
            "rating": random.randint(1, 5),
            "moderation_status": random.choice(moderation_statuses),
            "flags": [fake.word() for _ in range(random.randint(0, 2))],
            "submitted_at": submitted_at
        }
        data.append(document)
    db.ModerationQueue.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into ModerationQueue")

def generate_search_queries(num_docs=50):
    """Генерация коллекции SearchQueries."""
    data = []
    for _ in range(num_docs):
        timestamp = fake.date_time_between(start_date="-30d", end_date="now")
        filters_example = [fake.word() for _ in range(random.randint(0, 3))]  # имитация "фильтров"
        document = {
            "query_id": fake.uuid4(),
            "user_id": random.randint(1, 1000),
            "query_text": fake.word(),
            "timestamp": timestamp,
            "filters": filters_example,
            "results_count": random.randint(0, 200)
        }
        data.append(document)
    db.SearchQueries.insert_many(data)
    print(f"[OK] Inserted {num_docs} documents into SearchQueries")

if __name__ == "__main__":
    # На всякий случай очищаем коллекции перед вставкой, чтобы не дублировать
    db.UserSessions.delete_many({})
    db.ProductPriceHistory.delete_many({})
    db.EventLogs.delete_many({})
    db.SupportTickets.delete_many({})
    db.UserRecommendations.delete_many({})
    db.ModerationQueue.delete_many({})
    db.SearchQueries.delete_many({})

    generate_user_sessions()
    generate_product_price_history()
    generate_event_logs()
    generate_support_tickets()
    generate_user_recommendations()
    generate_moderation_queue()
    generate_search_queries()

    print("Data generation completed!")