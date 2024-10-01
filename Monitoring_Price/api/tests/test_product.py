import aiohttp
import asyncio

async def add_fake_product(session, product_id, base_url, product_url_template):
    product_url = product_url_template + str(product_id)
    try:
        async with session.post(f"{base_url}{product_url}") as response:
            if response.status == 200:
                print(f"Товар {product_id} успешно добавлен: {product_url}")
            else:
                print(f"Ошибка при добавлении товара {product_id}: {response.status} {await response.text()}")
    except Exception as e:
        print(f"Произошла ошибка при добавлении товара {product_id}: {e}")

async def add_fake_products(num_products):
    base_url = 'http://127.0.0.1:8000/products/?url='
    product_url_template = 'https://www.mvideo.ru/products/'

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, num_products + 1):
            tasks.append(add_fake_product(session, i, base_url, product_url_template))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(add_fake_products(100))
