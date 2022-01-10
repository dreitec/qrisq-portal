import requests
import base64

client_id = "******"
client_secret = "*****"

PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"
auth_token = None


def get_auth_token():
    global auth_token
    if auth_token is None:
        auth_code = (client_id + ":" + client_secret).encode('ascii')
        auth_code = base64.b64encode(auth_code).decode('ascii')
        headers = {
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept-Language': "en_US",
            'Authorization': "Basic {}".format(auth_code)
        }
        print(auth_code)
        body = "grant_type=client_credentials"
        url = PAYPAL_BASE_URL + "/v1/oauth2/token"
        r = requests.post(url, headers=headers, data=body)
        r.raise_for_status()
        response = r.json()
        auth_token = "Bearer {}".format(response["access_token"])
    return auth_token


def create_product():
    headers = {
        "Authorization": get_auth_token()
    }
    body = {
        "name": "qrisq-test-product",
        "description": "qrisq-test-product",
        "type": "SERVICE",
        "category": "SOFTWARE"
    }
    url = PAYPAL_BASE_URL + "/v1/catalogs/products"
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    return r.json()


def get_product():
    headers = {
        "Authorization": get_auth_token()
    }
    url = PAYPAL_BASE_URL + "/v1/catalogs/products"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["products"][0]


def create_plans(product_id):
    headers = {
        "Authorization": get_auth_token()
    }
    body = {
        "product_id": product_id,
        "name": "Monthly Plan",
        "description": "Monthly Plan",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": "5",
                        "currency_code": "USD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CANCEL",
            "payment_failure_threshold": 1
        },
        "taxes": {
            "percentage": "0",
            "inclusive": False
        }
    }
    url = PAYPAL_BASE_URL + "/v1/billing/plans"
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    print(r.json())
    body = {
        "product_id": product_id,
        "name": "Yearly Plan",
        "description": "Yearly Plan",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "Year",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": "20",
                        "currency_code": "USD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CANCEL",
            "payment_failure_threshold": 1
        },
        "taxes": {
            "percentage": "0",
            "inclusive": False
        }
    }
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    print(r.json())
    return r.json()


def get_plans(product_id):
    headers = {
        "Authorization": get_auth_token()
    }
    url = PAYPAL_BASE_URL + "/v1/billing/plans"
    query = {
        "product_id": product_id
    }
    r = requests.get(url, headers=headers, params=query)
    r.raise_for_status()
    return r.json()["plans"]



create_product()
product = get_product()
print(product)

create_plans(product["id"])
plans = get_plans(product["id"])


print(plans)




