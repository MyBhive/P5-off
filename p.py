

url = "https://fr.openfoodfacts.org/cgi/" \
      "search.pl?" \
      "action=process&" \
      "tagtype_0=categories&" \
      "tag_contains_0=contains&" \
      "tag_0={}}&" \
      "sort_by=unique_scans_n&page_size=1000&" \
      "axis_x=energy&" \
      "axis_y=products_n&action=display&json=1".format(CATEGORY[key])
response = requests.get(url)

bob = {
    "action": "process",
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "{}".format(CATEGORY[key]),
    "sort_by": "unique_scans_n",
    "page_size": "1000",
    "axis_x": "energy",
    "axis_y": "products_n",
    "action": "display",
    "json": "1"
           }

"https://bfr.openfoodfacts.org/cgi/search.pl"
payload = {
    "search_simple": "1",
    "action": "process",
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "{}".format(CATEGORY[key]),
    "sort_by": "ciqual_food_name_tags",
    "page_size": "200",
    "json": "1"
}

"https://fr.openfoodfacts.org/cgi/"
                        "search.pl?search_simple=1&"
                        "action=process&"
                        "tagtype_0=categories&"
                        "tag_contains_0=contains&"
                        "tag_0={}&"
                        "sort_by=ciqual_food_name_tags&"
                        "page_size=200&json=1".format(value))