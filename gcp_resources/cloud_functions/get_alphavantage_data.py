from urllib import request as urlrequest
import json
import os
import logging as log

base_url = "https://www.alphavantage.co"
api_key = os.environ['API_KEY']

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
    stock = request_json["symbol"]
    call = "%s/query?apikey=%s&outputsize=full&function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s" % (base_url, api_key, stock)

    try:
        with urlrequest.urlopen(call) as urlresponse:
            data = urlresponse.read().decode("utf-8")
            mydata = json.loads("".join(data))
            log.info(mydata)

            try:
                market_data = {
                    "metadata": mydata['Meta Data'],
                    "error": False,
                    "data": {},
                }

                for d in mydata['Time Series (Daily)']:
                    item = mydata['Time Series (Daily)'][d]
                    market_data["data"][d] = {}
                    for k in item:
                        market_data["data"][d][k.split(" ")[1]] = item[k]
                return json.dumps(market_data)
            except Exception as e:
                log.error(e)
                return '{"error": true}'
    except Exception as e:
        log.error(e)
        return "{}"

    return '{"error": true}'

