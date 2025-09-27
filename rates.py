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

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "x-csrf-token": "x",
        "cookie": 'marketing_vistor_id=463dccad-91c4-41e8-b2cd-ab98736ce6d8; udi-id=QHO0m23to6cQ6bykWFkVxcn3maAOqUD1Rq64zF/stUnJPO6RKvG6x9Rh2VGxeGOnMxuvXr1QJ2e6X/JOo0xbSQ6Je+o18/tUb7ytRqpJL4ybBbY2MPkIuVpvKUnViMYUeP8R9nYMbroeIn4PxAIzmxKsINfY6XpDakfgL+W1kOvpeb/cGndtJ5QzPKousjUbINOfk5u7GdUx6hXOmAN5Dg==9HmTCbP+TQeZc8jAwIExgw==odhETNUDFzrMVtxp4xNnqt/gcPCsaeHISOkvbgFp1qU=; sid=QA.CAESEOYIliTczkqzlQB9sO4jVp8Y0OSoxwYiATEqJGZlNjFjNjEwLTNiZGUtNGNiNi1hMTc1LTcwMTAzOTRmOTYwYzJAnKx5otbOMIu_sF4XigVEpp_BImBROnKJpv1zuomoyuhGd00_K2NvFw8k4lWHRfsKMW6RVR6WlrNW8mbu9j3M1DoBMUIIdWJlci5jb20.7w34RiKOE8Z3kmRxwBrIxsgbp1LueA30sb0yph4q9BA; smeta={"expiresAt":1760178768270}; csid=1.1760178768568.gEP0kavU4HBZxBUr0jzz9Ox/joaNEd4uUN3d/LXTyyE=; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NTgyMTEyODA1NTYsImNvb2tpZUNhdGVnb3JpZXMiOlsiZXNzZW50aWFsIl0sImltcGxpY2l0IjpmYWxzZX0%3D; UBER_CONSENTMGR=1758211280556|consent:false; _ua={"session_id":"1c5b613c-d21c-4087-a30a-52f81dbcb724","session_time_ms":1758211293686}; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NTgyMTMwOTM2ODYsIlVzZXItQWdlbnQiOiIiLCJ4LXViZXItY2xpZW50LWlkIjoiIiwieC11YmVyLWRldmljZSI6IiIsIngtdWJlci1jbGllbnQtdXNlci1zZXNzaW9uLWlkIjoiIiwidGVuYW5jeSI6InViZXIvcHJvZHVjdGlvbiJ9LCJpYXQiOjE3NTgyMTEyOTQsImV4cCI6MTc1ODI5NzY5NH0.F6ATPPkuyI8sJvhbyd86CGfEm2Fm4ozi5eaLeA5TEDg; _cc=ARdEFZCZsPKsmh1ttlXgfJof; _cid_cc=ARdEFZCZsPKsmh1ttlXgfJof; __cf_bm=Oqg5Rz56Msa0zlo3iNDA_6m2X5rlScdmIIYHLAxbWvw-1758213058-1.0.1.1-42iZ7IYABtbIRX5.lt82OGhbrkQQzU_pMRI_dfzsMXQyBASIxTJ7Jkb..ib3hrk3mN4aGIj_jzBcdcRaMMePQIIXNSkO8mWF0.S.r.c9224; mp_adec770be288b16d9008c964acfba5c2_mixpanel=%7B%22distinct_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%2C%22%24device_id%22%3A%20%221995d8f5c61be3-0387759cf15071-26061951-1aeaa0-1995d8f5c621f2b%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.uber.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.uber.com%22%2C%22%24user_id%22%3A%20%22fe61c610-3bde-4cb6-a175-7010394f960c%22%7D; udi-fingerprint=D37yt8QjfJUN6L6Ajn8Ul8DdLLrP8QxxOKDIW0ZKRC1APcWrYfWwlkRu+XkMyyZ5Fl5keOdi6eIDQjxLPsuyVw==xqiaxQbf3eAFZeQ2datOvHt426Kdz+K/oxSbZ81BpEQ=; city_id_cookie_key=805,2223',
        "x-uber-rv-session-type": "desktop_session",
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
                "latitude": coordinates["destination_lat"],
                "longitude": coordinates["destination_lng"],
            },
            "targetProductType": "CONNECT",
        },
        "query": "query Products($capacity: Int, $destinations: [InputCoordinate!]!, $includeRecommended: Boolean = false, $isRiderCurrentUser: Boolean, $payment: InputPayment, $paymentProfileUUID: String, $pickup: InputCoordinate!, $pickupFormattedTime: String, $profileType: String, $profileUUID: String, $returnByFormattedTime: String, $stuntID: String, $targetProductType: EnumRVWebCommonTargetProductType) {\n  products(\n    capacity: $capacity\n    destinations: $destinations\n    includeRecommended: $includeRecommended\n    isRiderCurrentUser: $isRiderCurrentUser\n    payment: $payment\n    paymentProfileUUID: $paymentProfileUUID\n    pickup: $pickup\n    pickupFormattedTime: $pickupFormattedTime\n    profileType: $profileType\n    profileUUID: $profileUUID\n    returnByFormattedTime: $returnByFormattedTime\n    stuntID: $stuntID\n    targetProductType: $targetProductType\n  ) {\n    ...ProductsFragment\n    __typename\n  }\n}\n\nfragment ProductsFragment on RVWebCommonProductsResponse {\n  defaultVVID\n  hourlyTiersWithMinimumFare {\n    ...HourlyTierFragment\n    __typename\n  }\n  intercity {\n    ...IntercityFragment\n    __typename\n  }\n  links {\n    iFrame\n    text\n    url\n    __typename\n  }\n  productsUnavailableMessage\n  tiers {\n    ...TierFragment\n    __typename\n  }\n  __typename\n}\n\nfragment BadgesFragment on RVWebCommonProductBadge {\n  backgroundColor\n  color\n  contentColor\n  icon\n  inactiveBackgroundColor\n  inactiveContentColor\n  text\n  __typename\n}\n\nfragment HourlyTierFragment on RVWebCommonHourlyTier {\n  description\n  distance\n  fare\n  fareAmountE5\n  farePerHour\n  minutes\n  packageVariantUUID\n  preAdjustmentValue\n  __typename\n}\n\nfragment IntercityFragment on RVWebCommonIntercityInfo {\n  oneWayIntercityConfig(destinations: $destinations, pickup: $pickup) {\n    ...IntercityConfigFragment\n    __typename\n  }\n  roundTripIntercityConfig(destinations: $destinations, pickup: $pickup) {\n    ...IntercityConfigFragment\n    __typename\n  }\n  __typename\n}\n\nfragment IntercityConfigFragment on RVWebCommonIntercityConfig {\n  description\n  onDemandAllowed\n  reservePickup {\n    ...IntercityTimePickerFragment\n    __typename\n  }\n  returnBy {\n    ...IntercityTimePickerFragment\n    __typename\n  }\n  __typename\n}\n\nfragment IntercityTimePickerFragment on RVWebCommonIntercityTimePicker {\n  bookingRange {\n    maximum\n    minimum\n    __typename\n  }\n  header {\n    subTitle\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment TierFragment on RVWebCommonProductTier {\n  products {\n    ...ProductFragment\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment ProductFragment on RVWebCommonProduct {\n  badges {\n    ...BadgesFragment\n    __typename\n  }\n  cityID\n  currencyCode\n  description\n  detailedDescription\n  discountPrimary\n  displayName\n  estimatedTripTime\n  etaStringShort\n  fares {\n    capacity\n    discountPrimary\n    fare\n    fareAmountE5\n    hasPromo\n    hasRidePass\n    meta\n    preAdjustmentValue\n    __typename\n  }\n  hasPromo\n  hasRidePass\n  hasBenefitsOnFare\n  hourly {\n    tiers {\n      ...HourlyTierFragment\n      __typename\n    }\n    overageRates {\n      ...HourlyOverageRatesFragment\n      __typename\n    }\n    __typename\n  }\n  iconType\n  id\n  is3p\n  isAvailable\n  legalConsent {\n    ...ProductLegalConsentFragment\n    __typename\n  }\n  parentProductUuid\n  preAdjustmentValue\n  productImageUrl\n  productUuid\n  reserveEnabled\n  __typename\n}\n\nfragment ProductLegalConsentFragment on RVWebCommonProductLegalConsent {\n  header\n  image {\n    url\n    width\n    __typename\n  }\n  description\n  enabled\n  ctaUrl\n  ctaDisplayString\n  buttonLabel\n  showOnce\n  shouldBlockRequest\n  __typename\n}\n\nfragment HourlyOverageRatesFragment on RVWebCommonHourlyOverageRates {\n  perDistanceUnit\n  perTemporalUnit\n  __typename\n}\n",
    }

    resp = requests.post(REQUEST_URL, json=payload, headers=headers)
    parsed_resp = resp.json()

    try:
        shipment_details = (
            parsed_resp.get("data").get("products").get("tiers")[0].get("products")
        )
        flash_price = shipment_details[0].get("fares")[0].get("fare")
        moto_price = shipment_details[1].get("fares")[0].get("fare")

        return flash_price, moto_price
    except AttributeError:
        return None
