import pandas as pd
import numpy as np
import http
import time
import json

from functools import reduce
from datetime import datetime
from bs4 import BeautifulSoup


# from xtlearn.utils import *

from urllib.error import HTTPError
from urllib.request import Request, urlopen


from tqdm import tqdm

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

CIDADES = [
    "al+maragogi",
    "ba+feira-de-santana",
    "es+vila-velha",
    "es+vitoria",
    "mg+mateus-leme",
    "mg+montes-claros",
    "mg+uberaba",
    "mt+varzea-grande",
    "pr+londrina",
    "rj+buzios",
    "rj+rio-de-janeiro",
    "sp+campinas",
    "sp+jaguariuna",
    "sp+presidente-prudente",
    "sp+sao-jose-do-rio-preto",
    "sp+sao-jose-dos-campos",
    "sp+sao-paulo",
    "sp+tanabi",
    "sp+valinhos",
]

TABLE_COLUMNS = [
    "search_id",
    "search_date",
    "seacrh_action",
    "search_type",
    "search_localization",
    "search_page",
    "search_id",
    "displayAddressType",
    "amenities",
    "usableAreas",
    "constructionStatus",
    "listingType",
    "description",
    "title",
    "stamps",
    "createdAt",
    "floors",
    "unitTypes",
    "nonActivationReason",
    "providerId",
    "propertyType",
    "unitSubTypes",
    "unitsOnTheFloor",
    "legacyId",
    "id",
    "portal",
    "unitFloor",
    "parkingSpaces",
    "updatedAt",
    "address_country",
    "address_zipCode",
    "address_geoJson",
    "address_city",
    "address_streetNumber",
    "address_level",
    "address_precision",
    "address_confidence",
    "address_stateAcronym",
    "address_source",
    "point_lon",
    "point_source",
    "point_lat",
    "address_ibgeCityId",
    "address_zone",
    "address_street",
    "address_locationId",
    "address_district",
    "address_name",
    "address_state",
    "address_neighborhood",
    "address_poisList",
    "address_complement",
    "address_pois",
    "address_valuableZones",
    "valuableZones_city",
    "valuableZones_zone",
    "valuableZones_name",
    "valuableZones_id",
    "valuableZones_state",
    "valuableZones_category",
    "suites",
    "publicationType",
    "externalId",
    "bathrooms",
    "usageTypes",
    "totalAreas",
    "whatsappNumber",
    "bedrooms",
    "acceptExchange",
    "pricingInfos_yearlyIptu",
    "pricingInfos_price",
    "pricingInfos_businessType",
    "pricingInfos_monthlyCondoFee",
    "showPrice",
    "resale",
    "buildings",
    "capacityLimit",
    "status",
    "hasAddress",
    "isDevelopment",
    "isInactive",
    "isDefaulterInactive",
    "pricingInfos",
    "pricingInfo_monthlyCondoFee",
    "pricingInfo_period",
    "pricingInfo_price",
    "pricingInfo_rentalPrice",
    "pricingInfo_rentalTotalPrice",
    "pricingInfo_salePrice",
    "pricingInfo_showPrice",
    "pricingInfo_yearlyIptu",
    "pricingInfo_priceVariation",
    "pricingInfo_warranties",
    "pricingInfo_businessType",
    "pricingInfo_businessLabel",
    "pricingInfo_businessDescription",
    "pricingInfo_isSale",
    "pricingInfo_isRent",
    "subtitle",
    "businessTypeContext",
    "preview",
    "showPhoneButton",
    "link",
    "isSpecialRent",
    "rentalInfo_period",
    "rentalInfo_warranties",
]


def get_page(url: str, timeout: int = 20, verbose: int = 0):
    """Make a request to a site html and returns the html code

    :param url: URL from the desired site
    :type url: str
    :param timeout: Maximum time in seconds to wait the response, defaults to 20
    :type timeout: int, optional
    :param verbose: Logging level, defaults to 0
    :type verbose: int, optional
    :return: The site htto response
    :rtype: http.client.HTTPResponse
    """

    request = Request(url)

    request.add_header("User-Agent", USER_AGENT)

    try:
        response = urlopen(request, timeout=timeout)
    except HTTPError as e:
        if verbose > 0:
            print("[error]", e)

        if e.getcode() == 400:
            response = None
        elif e.getcode() == 404:
            response = None

    return response


def get_total(action: str, type: str, localization: str, timeout: int = 20):
    """Scrappes an returns the total estates available in zapimoveis.com.br for an specified action and type.

    :param action: Action related to the estate. ('venda' ou 'aluguel')
    :type action: str
    :param type: Estate type. ('imoveis', 'casas', 'apartamentos', 'terrenos-lotes-condominios')
    :type type: str
    :param localization: State and city in the format 'st+city' where city name is sclitted by '-'. Example: sp+sao-paulo
    :type localization: str
    :param timeout: Maximum time in seconds for request, defaults to 20
    :type timeout: int, optional
    :return: The number of available estates
    :rtype: int
    """

    url = f"https://www.zapimoveis.com.br/{action}/{type}/{localization}"

    html = get_page(url, timeout=timeout)

    soup = BeautifulSoup(html, "html.parser")

    return int(
        soup.find("h1", {"class": ["summary__title", "js-summary-title"]})
        .find("strong")
        .text.split()[0]
        .replace(".", "")
    )


def get_listings(soup: BeautifulSoup):
    """Get listings from zap-imoves web page

    :param soup: Beaturiful soup instance
    :type soup: BeautifulSoup
    :return: List of listings
    :rtype: lists
    """

    page_data_string = soup.find(
        lambda tag: tag.name == "script"
        and isinstance(tag.string, str)
        and tag.string.startswith("window")
    )

    json_string = page_data_string.string.replace(
        "window.__INITIAL_STATE__=", ""
    ).replace(
        ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());",
        "",
    )

    return json.loads(json_string)["results"]["listings"]


def search_page(
    action: str,
    state_type: str,
    localization: str,
    page: int,
    timeout: int = 20,
    verbose: int = 0,
):
    """Get a list of listing properties from a zap-imoveis page

    :param action: Action related to the estate. ('venda' ou 'aluguel')
    :type action: str
    :param state_type: Estate type. ('imoveis', 'casas', 'apartamentos', 'terrenos-lotes-condominios')
    :type state_type: str
    :param localization: State and city in the format 'st+city' where city name is sclitted by '-'. Example: sp+sao-paulo
    :type localization: str
    :param page: Page number
    :type page: int
    :param timeout: Maximum time in seconds for request, defaults to 20
    :type timeout: int, optional
    :param verbose: Logging level, defaults to 0
    :type verbose: int, optional
    :return: List of listings
    :rtype: list
    """
    url = f"https://www.zapimoveis.com.br/{action}/{state_type}/{localization}/?pagina={page}"

    html = get_page(url, timeout=timeout, verbose=verbose)

    if html is not None:

        soup = BeautifulSoup(html, "html.parser")

        results = get_listings(soup)

    else:
        results = None

    return results


def get_dict_info(dictionary, key, prefix=""):

    if type(dictionary[key]) == dict:
        result = {}

        for k in dictionary[key].keys():
            result.update(get_dict_info(dictionary[key], k, prefix=key + "_"))
    else:
        result = {prefix + key: dictionary[key]}

    return result


def format_dict(
    elem,
    keys_to_drop=[
        "images",
        "videos",
        "videoTour",
        "advertiserContact_phones",
        "advertiserContact_chat",
        "advertiserContact_phones",
        "advertiserId",
    ],
):
    elem["pricingInfos"] = expand_list_key(elem, "pricingInfos")
    elem["address"]["valuableZones"] = expand_list_key(elem["address"], "valuableZones")

    elem["usableAreas"] = (
        str(elem["usableAreas"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["totalAreas"] = (
        str(elem["usableAreas"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["amenities"] = (
        str(elem["amenities"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["usageTypes"] = (
        str(elem["usageTypes"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["parkingSpaces"] = (
        str(elem["parkingSpaces"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["bathrooms"] = (
        str(elem["bathrooms"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["bedrooms"] = (
        str(elem["bedrooms"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    elem["suites"] = (
        str(elem["suites"])
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "|")
    )

    if type(elem["address"]["poisList"]) == list:
        if elem["address"]["poisList"] != []:

            elem["address"]["poisList"] = reduce(
                lambda x, y: str(x) + "|" + str(y), elem["address"]["poisList"]
            )

    result = {}

    for key in elem.keys():
        result.update(get_dict_info(elem, key, prefix=""))

    for k in keys_to_drop:
        if k in result.keys():
            result.pop(k)

    return result


def expand_list_key(dictionary: dict, key: str):

    result = dictionary[key]

    if type(result) == list:
        if len(result) > 0:
            result = reduce(lambda x, y: x.update(y), result)

    return result


def expand_unique_element_list(dictionary):
    for k in dictionary.keys():
        if type(dictionary[k]) == list:
            if len(dictionary[k]) == 1:
                val = dictionary[k][0]
                dictionary[k] = val
            elif len(dictionary[k]) == 0:
                dictionary[k] = None

        elif type(dictionary[k]) == dict:
            dictionary[k] = expand_unique_element_list(dictionary[k])

    return dictionary


def format_search(info, action, state_type, localization, page):

    if info is None:
        return []
    else:
        list_ = []

        for i in info:

            date_today = datetime.now()

            elem = i["listing"]

            elem.update(
                {
                    "search_id": str(elem["id"])
                    + "__"
                    + str(datetime.strftime(date_today, "%Y_%m_%d_%H_%M_%S"))
                    #                     + "__"
                    #                     + str(int(1000 * np.random.random()))
                }
            )
            elem.update({"search_date": date_today.isoformat()})
            elem.update({"seacrh_action": action})
            elem.update({"search_type": state_type})
            elem.update({"search_localization": localization})
            elem.update({"search_page": page})

            result = format_dict(elem)
            result = expand_unique_element_list(result)

            list_.append(result)

        return list_


def search(
    page_list: list,
    localization: str = "sp+sao-paulo",
    action: str = "venda",
    type: str = "casas",
    sleep_time_bias: float = 5,
    sleep_time_mean: float = 2,
    sleep_time_std: float = 1,
    timeout: int = 20,
    engine=None,
    table=None,
    export_to_sql=False,
):

    empty_df = pd.DataFrame({col: [] for col in TABLE_COLUMNS})

    results = pd.DataFrame({col: [] for col in TABLE_COLUMNS})

    for page in tqdm(page_list, total=len(page_list), desc="Scrapping"):

        params = {
            "action": action,
            "state_type": type,
            "localization": localization,
            "page": page,
        }

        search_result = search_page(timeout=timeout, **params)

        time.sleep(simulated_time(sleep_time_mean, sleep_time_std, sleep_time_bias))

        info = pd.DataFrame(format_search(search_result, **params))

        df_dados = empty_df.append(info).set_index("search_id")

        for col in df_dados:
            try:
                df_dados[col] = df_dados[col].apply(str)
            except:
                pass

        results = results.append(df_dados.reset_index())

    return results


def simulated_time(mu: float, std: float, val: float):
    sleep_time = np.random.normal(mu, std, 1)
    sleep_time = np.where(sleep_time > 0, sleep_time, 0)

    t = 0
    t = val * np.random.random()
    t = np.where(t > val - 1, val, 0)

    sleep_time = sleep_time + t

    return sleep_time[0]
