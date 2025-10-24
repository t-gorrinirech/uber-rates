import googlemaps
import requests

from my_secrets import *

REQUEST_URL = "https://m.uber.com/go/graphql"


def get_rates(origin, destination):
    gmaps = googlemaps.Client(key=API_KEY)
    origin_geocode = gmaps.geocode(origin)
    destination_geocode = gmaps.geocode(destination)

    if len(origin_geocode) < 1 or len(destination_geocode) < 1:
        return None

    coordinates = {
        "origin_lat": origin_geocode[0].get("geometry").get("location").get("lat"),
        "origin_lng": origin_geocode[0].get("geometry").get("location").get("lng"),
        "destination_lat": destination_geocode[0]
        .get("geometry")
        .get("location")
        .get("lat"),
        "destination_lng": destination_geocode[0]
        .get("geometry")
        .get("location")
        .get("lng"),
    }

    cookies = {
        "marketing_vistor_id": "62b3255e-d728-40a1-a097-a91a604b0a9b",
        "udi-id": "VbbajthoPHJlreWHMhOmWEmWZ+GVoWSplxiJkpKRsaVcc5mWxBXensbQvTIJW4c2cK4EkamtMpx1sw8UcI+UGcMM+OMXarCWYUhRx+hSVW/mXvjgYzdxoB0oZ2FZej3QQCXCQnRVO/XPkPBwTe/yIhJJF815S3DQyggrNAsZJa6ysipwG/ZEBk36E/RXGF2m5XxY5Dav7wiIRCxU9VWZ3w==FWVHYaWO46GY/ayqO2sOqA==NrVkBtaZhnewWmAI8GHPPAO9FQp7EpErONN4FfKczHM=",
        "sid": "QA.CAESECH67U0H0kG_o_9oRTdUyeYYyvGvyAYiATEqJGZlNjFjNjEwLTNiZGUtNGNiNi1hMTc1LTcwMTAzOTRmOTYwYzJACBskLi7eXAbYAZVZw0tlBJ9mfi4SwocQiAmh1d8KGWaitbKrusJ6IQpPA7VRrCxfFZYubMK3Uuq7ATGZrFhYgDoBMUIIdWJlci5jb20.deK2l7q8r_qxhMCYtXfRMjo-dPkJZVjfvEAtXiXhzWY",
        "smeta": '{"expiresAt":1762392266804}',
        "csid": "1.1762392267089.lfTo10gMOldjKRbAf5xIbIqroOzKlyn/GNhkhOdbFGk=",
        "_cc": "AUXAUte6zQU6kUFw7HyXNGkC",
        "_cid_cc": "AUXAUte6zQU6kUFw7HyXNGkC",
        "u-cookie-prefs": "eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NTk4MDAzODgwOTIsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0IjpmYWxzZX0%3D",
        "CONSENTMGR": "1759800388100|consent:true",
        "UBER_CONSENTMGR": "1759800388100|consent:true",
        "_fbp": "fb.1.1759800388117.455572488359533415.Bg",
        "__cf_bm": "Fr86q5f_Dou2MvfrJA5GWTBbHWzdyUUoMfPo4lEEdfQ-1760468448-1.0.1.1-dlfUlSJBH7Tlcjx1bNT4_3AbhpQR7LSvM.ouL31wBY60v7e9eNwPA1IOGx19L5WMYMIcyfBSQhhE04rrLonsO6QK7oWqc8RCzcxlJqFExQs",
        "utag_main__sn": "3",
        "utag_main_ses_id": "1760468570854%3Bexp-session",
        "utag_main__ss": "0%3Bexp-session",
        "_ua": '{"session_id":"da7cdaa9-207f-46e3-83a1-d1728ea6a1c8","session_time_ms":1760468496531}',
        "city_id_cookie_key": "805",
        "jwt-session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NjA0NzAyOTY1MzMsIlVzZXItQWdlbnQiOiIiLCJ4LXViZXItY2xpZW50LWlkIjoiIiwieC11YmVyLWRldmljZSI6IiIsIngtdWJlci1jbGllbnQtdXNlci1zZXNzaW9uLWlkIjoiIiwidGVuYW5jeSI6InViZXIvcHJvZHVjdGlvbiJ9LCJpYXQiOjE3NjA0MDUwNTcsImV4cCI6MTc2MDQ5MTQ1N30.PZZElnw4xnVZyGHdNuPMsktIxZADJETTnEBjJcO74jM",
        "utag_main__pn": "2%3Bexp-session",
        "mp_adec770be288b16d9008c964acfba5c2_mixpanel": "%7B%22distinct_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%2C%22%24device_id%22%3A%20%22199bc46d1d7248e-0612b7199299dc8-26061951-1fa400-199bc46d1d828dc%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fauth.uber.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22auth.uber.com%22%2C%22%24user_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%7D",
        "udi-fingerprint": "yd+/8/JgEObCgv36rNcfHI8Bto+wpcU7CRKT+2TjM3QqU4+IpC8kHBOPAVUTEDdQjmF5KHaqv3OgHfR8uKgYMA==+ACIr+ED8VK2Gw0Zm12y7CpgpJSnoG3vgNL4GrI40q4=",
        "utag_main__se": "8%3Bexp-session",
        "utag_main__st": "1760470424554%3Bexp-session",
    }

    headers = {
        "accept": "*/*",
        "accept-language": "es-ES,es;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://m.uber.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://m.uber.com/go/connect/product-selection?drop%5B0%5D=%7B%22addressLine1%22%3A%22Jujuy%22%2C%22addressLine2%22%3A%22Bernal%2C%20Provincia%20de%20Buenos%20Aires%22%2C%22id%22%3A%22EjNKdWp1eSwgQmVybmFsLCBQcm92aW5jaWEgZGUgQnVlbm9zIEFpcmVzLCBBcmdlbnRpbmEiLiosChQKEglzuFLW5S2jlRHzW8G0UtmrZBIUChIJXd0Lx_0xo5URrKtd8fMscGw%22%2C%22source%22%3A%22SEARCH%22%2C%22latitude%22%3A-34.7191098%2C%22longitude%22%3A-58.2778439%2C%22provider%22%3A%22google_places%22%7D&pickup=%7B%22addressLine1%22%3A%22Fray%20Mamerto%20Esqui%C3%BA%201600%22%2C%22addressLine2%22%3A%22B1826GBT%20Buenos%20Aires%2C%20Provincia%20de%20Buenos%20Aires%22%2C%22id%22%3A%22ChIJKWcLMTTNvJURjL81vF0ElkI%22%2C%22source%22%3A%22SEARCH%22%2C%22latitude%22%3A-34.712635%2C%22longitude%22%3A-58.37647010000001%2C%22provider%22%3A%22google_places%22%7D&uclick_id=d9eeeea3-78de-48db-b591-50a89e2051af",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "x-csrf-token": "x",
        "x-uber-rv-initial-load-city-id": "805",
        "x-uber-rv-session-type": "desktop_session",
        # 'cookie': 'marketing_vistor_id=62b3255e-d728-40a1-a097-a91a604b0a9b; udi-id=VbbajthoPHJlreWHMhOmWEmWZ+GVoWSplxiJkpKRsaVcc5mWxBXensbQvTIJW4c2cK4EkamtMpx1sw8UcI+UGcMM+OMXarCWYUhRx+hSVW/mXvjgYzdxoB0oZ2FZej3QQCXCQnRVO/XPkPBwTe/yIhJJF815S3DQyggrNAsZJa6ysipwG/ZEBk36E/RXGF2m5XxY5Dav7wiIRCxU9VWZ3w==FWVHYaWO46GY/ayqO2sOqA==NrVkBtaZhnewWmAI8GHPPAO9FQp7EpErONN4FfKczHM=; sid=QA.CAESECH67U0H0kG_o_9oRTdUyeYYyvGvyAYiATEqJGZlNjFjNjEwLTNiZGUtNGNiNi1hMTc1LTcwMTAzOTRmOTYwYzJACBskLi7eXAbYAZVZw0tlBJ9mfi4SwocQiAmh1d8KGWaitbKrusJ6IQpPA7VRrCxfFZYubMK3Uuq7ATGZrFhYgDoBMUIIdWJlci5jb20.deK2l7q8r_qxhMCYtXfRMjo-dPkJZVjfvEAtXiXhzWY; smeta={"expiresAt":1762392266804}; csid=1.1762392267089.lfTo10gMOldjKRbAf5xIbIqroOzKlyn/GNhkhOdbFGk=; _cc=AUXAUte6zQU6kUFw7HyXNGkC; _cid_cc=AUXAUte6zQU6kUFw7HyXNGkC; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NTk4MDAzODgwOTIsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0IjpmYWxzZX0%3D; CONSENTMGR=1759800388100|consent:true; UBER_CONSENTMGR=1759800388100|consent:true; _fbp=fb.1.1759800388117.455572488359533415.Bg; __cf_bm=Fr86q5f_Dou2MvfrJA5GWTBbHWzdyUUoMfPo4lEEdfQ-1760468448-1.0.1.1-dlfUlSJBH7Tlcjx1bNT4_3AbhpQR7LSvM.ouL31wBY60v7e9eNwPA1IOGx19L5WMYMIcyfBSQhhE04rrLonsO6QK7oWqc8RCzcxlJqFExQs; utag_main__sn=3; utag_main_ses_id=1760468570854%3Bexp-session; utag_main__ss=0%3Bexp-session; _ua={"session_id":"da7cdaa9-207f-46e3-83a1-d1728ea6a1c8","session_time_ms":1760468496531}; city_id_cookie_key=805; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NjA0NzAyOTY1MzMsIlVzZXItQWdlbnQiOiIiLCJ4LXViZXItY2xpZW50LWlkIjoiIiwieC11YmVyLWRldmljZSI6IiIsIngtdWJlci1jbGllbnQtdXNlci1zZXNzaW9uLWlkIjoiIiwidGVuYW5jeSI6InViZXIvcHJvZHVjdGlvbiJ9LCJpYXQiOjE3NjA0MDUwNTcsImV4cCI6MTc2MDQ5MTQ1N30.PZZElnw4xnVZyGHdNuPMsktIxZADJETTnEBjJcO74jM; utag_main__pn=2%3Bexp-session; mp_adec770be288b16d9008c964acfba5c2_mixpanel=%7B%22distinct_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%2C%22%24device_id%22%3A%20%22199bc46d1d7248e-0612b7199299dc8-26061951-1fa400-199bc46d1d828dc%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fauth.uber.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22auth.uber.com%22%2C%22%24user_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%7D; udi-fingerprint=yd+/8/JgEObCgv36rNcfHI8Bto+wpcU7CRKT+2TjM3QqU4+IpC8kHBOPAVUTEDdQjmF5KHaqv3OgHfR8uKgYMA==+ACIr+ED8VK2Gw0Zm12y7CpgpJSnoG3vgNL4GrI40q4=; utag_main__se=8%3Bexp-session; utag_main__st=1760470424554%3Bexp-session',
    }

    payload = {
        "operationName": "Products",
        "variables": {
            "includeRecommended": False,
            "destinations": [
                {
                    "latitude": coordinates["destination_lat"],
                    "longitude": coordinates["destination_lng"],
                }
            ],
            "payment": {"paymentProfileUUID": "4bd25017-b68c-5625-9d3a-3c810e6cb60c"},
            "paymentProfileUUID": "4bd25017-b68c-5625-9d3a-3c810e6cb60c",
            "pickup": {
                "latitude": coordinates["origin_lat"],
                "longitude": coordinates["origin_lng"],
            },
            "targetProductType": "CONNECT",
        },
        "query": "query Products($capacity: Int, $destinations: [InputCoordinate!]!, $includeRecommended: Boolean = false, $isRiderCurrentUser: Boolean, $payment: InputPayment, $paymentProfileUUID: String, $pickup: InputCoordinate!, $pickupFormattedTime: String, $profileType: String, $profileUUID: String, $returnByFormattedTime: String, $stuntID: String, $targetProductType: EnumRVWebCommonTargetProductType) {\n  products(\n    capacity: $capacity\n    destinations: $destinations\n    includeRecommended: $includeRecommended\n    isRiderCurrentUser: $isRiderCurrentUser\n    payment: $payment\n    paymentProfileUUID: $paymentProfileUUID\n    pickup: $pickup\n    pickupFormattedTime: $pickupFormattedTime\n    profileType: $profileType\n    profileUUID: $profileUUID\n    returnByFormattedTime: $returnByFormattedTime\n    stuntID: $stuntID\n    targetProductType: $targetProductType\n  ) {\n    ...ProductsFragment\n    __typename\n  }\n}\n\nfragment ProductsFragment on RVWebCommonProductsResponse {\n  defaultVVID\n  hourlyTiersWithMinimumFare {\n    ...HourlyTierFragment\n    __typename\n  }\n  intercity {\n    ...IntercityFragment\n    __typename\n  }\n  links {\n    iFrame\n    text\n    url\n    __typename\n  }\n  productsUnavailableMessage\n  tiers {\n    ...TierFragment\n    __typename\n  }\n  __typename\n}\n\nfragment BadgesFragment on RVWebCommonProductBadge {\n  backgroundColor\n  color\n  contentColor\n  icon\n  inactiveBackgroundColor\n  inactiveContentColor\n  text\n  __typename\n}\n\nfragment HourlyTierFragment on RVWebCommonHourlyTier {\n  description\n  distance\n  fare\n  fareAmountE5\n  farePerHour\n  minutes\n  packageVariantUUID\n  preAdjustmentValue\n  __typename\n}\n\nfragment IntercityFragment on RVWebCommonIntercityInfo {\n  oneWayIntercityConfig(destinations: $destinations, pickup: $pickup) {\n    ...IntercityConfigFragment\n    __typename\n  }\n  roundTripIntercityConfig(destinations: $destinations, pickup: $pickup) {\n    ...IntercityConfigFragment\n    __typename\n  }\n  __typename\n}\n\nfragment IntercityConfigFragment on RVWebCommonIntercityConfig {\n  description\n  onDemandAllowed\n  reservePickup {\n    ...IntercityTimePickerFragment\n    __typename\n  }\n  returnBy {\n    ...IntercityTimePickerFragment\n    __typename\n  }\n  __typename\n}\n\nfragment IntercityTimePickerFragment on RVWebCommonIntercityTimePicker {\n  bookingRange {\n    maximum\n    minimum\n    __typename\n  }\n  header {\n    subTitle\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment TierFragment on RVWebCommonProductTier {\n  products {\n    ...ProductFragment\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment ProductFragment on RVWebCommonProduct {\n  badges {\n    ...BadgesFragment\n    __typename\n  }\n  cityID\n  currencyCode\n  description\n  detailedDescription\n  discountPrimary\n  displayName\n  estimatedTripTime\n  etaStringShort\n  fares {\n    capacity\n    discountPrimary\n    fare\n    fareAmountE5\n    hasPromo\n    hasRidePass\n    meta\n    preAdjustmentValue\n    __typename\n  }\n  hasPromo\n  hasRidePass\n  hasBenefitsOnFare\n  hourly {\n    tiers {\n      ...HourlyTierFragment\n      __typename\n    }\n    overageRates {\n      ...HourlyOverageRatesFragment\n      __typename\n    }\n    __typename\n  }\n  iconType\n  id\n  is3p\n  isAvailable\n  legalConsent {\n    ...ProductLegalConsentFragment\n    __typename\n  }\n  parentProductUuid\n  preAdjustmentValue\n  productImageUrl\n  productUuid\n  reserveEnabled\n  __typename\n}\n\nfragment ProductLegalConsentFragment on RVWebCommonProductLegalConsent {\n  header\n  image {\n    url\n    width\n    __typename\n  }\n  description\n  enabled\n  ctaUrl\n  ctaDisplayString\n  buttonLabel\n  showOnce\n  shouldBlockRequest\n  __typename\n}\n\nfragment HourlyOverageRatesFragment on RVWebCommonHourlyOverageRates {\n  perDistanceUnit\n  perTemporalUnit\n  __typename\n}\n",
    }

    resp = requests.post(REQUEST_URL, json=payload, headers=headers, cookies=cookies)
    parsed_resp = resp.json()

    try:
        shipment_details = (
            parsed_resp.get("data").get("products").get("tiers")[0].get("products")
        )
        flash_price = shipment_details[0].get("fares")[0].get("fare")
        moto_price = shipment_details[1].get("fares")[0].get("fare")

        return {"precioAuto": flash_price, "precioMoto": moto_price}
    except AttributeError:
        return None
