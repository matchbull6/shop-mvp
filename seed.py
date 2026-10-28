import os
import random

import faker_commerce
import httpx
from faker import Faker

API_URL = os.environ["API_URL"]
API_KEY = os.environ["API_KEY"]
MAX_NAME_LENGTH = 100
COUNT = 50

ids = random.sample(range(1, 100_001), COUNT)

fake = Faker()
fake.add_provider(faker_commerce.Provider)


def random_name() -> str:
    name = f"{fake.unique.ecommerce_name()}, {fake.safe_color_name()}, {fake.catch_phrase().lower()}"
    return name[:MAX_NAME_LENGTH]


with httpx.Client(timeout=30, follow_redirects=True) as client:
    for id in ids:
        image = client.get(f"https://picsum.photos/seed/{id}/600.jpg")
        image.raise_for_status()

        response = client.post(
            f"{API_URL}/api/products",
            headers={"X-API-Key": API_KEY},
            data={"name": random_name()},
            files={"image": ("photo.jpg", image.content, "image/jpeg")},
        )
        response.raise_for_status()
        print(f"Создан Товар {id}")
