from lxml import html
import requests

def get_calories(search):

    search = search.replace(" ", "+")

    page = requests.get('http://www.fatsecret.com/calories-nutrition/search?q={}'.format(search))
    tree = html.fromstring(page.content)

    result_link = tree.xpath('//a[@class="prominent"]/@href')[0]
    page2 = requests.get("http://www.fatsecret.com{}".format(result_link))
    tree2 = html.fromstring(page2.content)

    food = {
        'name': search,
        'link': result_link,
        'total': float(tree2.xpath('//div[@class="factValue"]/text()')[0]),
        'fat': float(tree2.xpath('//div[@class="factValue"]/text()')[1].strip("g")),
        'carbs': float(tree2.xpath('//div[@class="factValue"]/text()')[2].strip("g")),
        'protein': float(tree2.xpath('//div[@class="factValue"]/text()')[3].strip("g"))
    }

    return food
