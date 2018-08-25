from urllib import request as urlrequest
import json
import os
import logging as log

base_url = "https://query1.finance.yahoo.com/v7"

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>`.
    """ 
    request_json = request.get_json()
    symbol = request_json["symbol"]
    call = "%s/finance/options/%s" % (base_url, symbol)

    if "expiration" in request_json:
        call = "%s?date=%s" % (call, request_json["expiration"])

    try:
        with urlrequest.urlopen(call) as urlresponse:
            data = urlresponse.read().decode("utf-8")
            mydata = json.loads("".join(data))['optionChain']['result'][0]

            try:
                market_data = {
                    "quote": mydata['quote'],
                    "expirationDates": mydata['expirationDates'],
                    "options": {}
                }

                if "nearMoney" in request_json:
                    quote_price = market_data["quote"]["ask"]
                    mf = quote_price * request_json["nearMoney"]

                    for ch in mydata["options"]:
                        market_data["options"][ch["expirationDate"]] = {
                            "calls": [i for i in ch["calls"] if i["strike"] < quote_price + mf and i["strike"] > (quote_price - mf) ],
                            "puts":  [i for i in ch["puts"]  if i["strike"] > quote_price - mf and i["strike"] < (quote_price + mf) ],
                        }
                else:
                    for ch in mydata["options"]:
                        market_data["options"][ch["expirationDate"]] = {
                            "calls": ch["calls"],
                            "puts":  ch["puts"]
                        }

                return json.dumps(market_data)
            except Exception as e:
                log.error(e)
    except Exception as e:
        log.error(e)

    return '{"error": true}'
