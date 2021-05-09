import json
import requests
from bs4 import BeautifulSoup
from flask import Flask


def get_defi(page: int = None):
    URL = "https://www.coingecko.com/en/defi"
    if page:
        URL = URL + f"?page={page}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(attrs={"data-target": "gecko-table.table"}).find_all("tr")

    output_dict = []

    for row in rows[1:]:
        token_name = row.find("i")["data-coin-symbol"].upper()
        token_price = row.find(attrs={"data-target": "price.price"}).text
        mcap = row.find("td", class_="text-right col-market").find(
            attrs={"data-target": "price.price"}
        )
        if mcap:
            mcap = mcap.text
        output_dict.append(
            {"token": token_name, "price": token_price, "marketCap": mcap}
        )

    return output_dict


app = Flask(__name__)


@app.route("/")
def index():
    return json.dumps(get_defi(), indent=2)


@app.route("/page/<int:page_number>")
def with_page(page_number: int):
    if page_number not in [1, 2, 3]:
        page_number = 1

    return json.dumps(get_defi(page=page_number), indent=2)
