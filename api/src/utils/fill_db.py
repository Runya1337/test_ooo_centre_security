import requests


def add_fake_product(product_id, base_url, product_url_template):
    product_url = product_url_template + str(product_id)
    try:
        response = requests.post(f"{base_url}/products/", params={"url": product_url})
        if response.status_code == 200:
            product_data = response.json()
            product_id_in_db = product_data["id"]
            print(f"Товар {product_id_in_db} успешно добавлен: {product_url}")
            return product_id_in_db
        else:
            print(
                f"Ошибка при добавлении товара {product_id}: {response.status_code} {response.text}"
            )
    except Exception as e:
        print(f"Произошла ошибка при добавлении товара {product_id}: {e}")


def add_fake_price_history(product_id, base_url):
    try:
        response = requests.post(
            f"{base_url}/products/products/{product_id}/fake_history/", json={}
        )
        if response.status_code == 200:
            print(f"История цен для товара {product_id} успешно добавлена")
        else:
            print(
                f"Ошибка при добавлении истории цен для товара {product_id}: {response.status_code} {response.text}"
            )
    except Exception as e:
        print(
            f"Произошла ошибка при добавлении истории цен для товара {product_id}: {e}"
        )


def add_fake_products(num_products):
    base_url = "http://127.0.0.1:8000"
    product_url_template = "https://www.mvideo.ru/products/"

    product_ids = []
    for i in range(1, num_products + 1):
        product_id = add_fake_product(i, base_url, product_url_template)
        if product_id:
            product_ids.append(product_id)

    for product_id in product_ids:
        add_fake_price_history(product_id, base_url)


if __name__ == "__main__":
    NUM_PRODUCTS = 15
    add_fake_products(NUM_PRODUCTS)
