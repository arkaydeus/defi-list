import json
import requests
from bs4 import BeautifulSoup
from flask import Flask


def get_defi():
    URL = "https://www.coingecko.com/en/defi"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find(attrs={"data-target": "gecko-table.table"}).find_all("tr")

    output_dict = []

    for row in rows[1:]:
        token_name = row.find("i")["data-coin-symbol"].upper()
        token_price = row.find(attrs={"data-target": "price.price"}).text
        mcap = (
            row.find("td", class_="text-right col-market")
            .find(attrs={"data-target": "price.price"})
            .text
        )
        output_dict.append(
            {"token": token_name, "price": token_price, "marketCap": mcap}
        )

    return output_dict


app = Flask(__name__)


@app.route("/")
def index():
    return json.dumps(get_defi(), indent=2)
