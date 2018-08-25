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
    symbol = ",".join(request_json["symbols"])
    call = "%s/finance/quote?symbols=%s" % (base_url, symbol)

    try:
        with urlrequest.urlopen(call) as urlresponse:
            data = urlresponse.read().decode("utf-8")
            mydata = json.loads("".join(data))
            log.info(mydata)

            try:
                market_data = {
                    d["symbol"]: d for d in mydata['quoteResponse']['result']
                }
                return json.dumps(market_data)
            except Exception as e:
                log.error(e)
                return '{"error": true}'
    except Exception as e:
        log.error(e)
        return "{}"

    return '{"error": true}'
