# flask - API handler
import datetime
from forex_python.converter import CurrencyRates
from flask import Flask, request, jsonify
from decimal import Decimal

app = Flask(__name__)


@app.route("/rates/<string:currency>", methods=['GET'])
def get_currency_rates(currency):
    """
    The flask API for getting the rate of the currency.
    :param currency:
    :return:
    """
    cur_rates_obj = CurrencyRates()

    target_cur = request.args.get('target')
    finding_date = request.args.get('date')

    if currency and target_cur and finding_date:
        date_obj = datetime.datetime.strptime(finding_date,
                                              '%d-%m-%Y,%H:%M:%S')
        rate_value = cur_rates_obj.get_rate(currency, target_cur, date_obj)

    elif currency and target_cur and not finding_date:
        rate_value = cur_rates_obj.get_rate(currency, target_cur)

    elif currency and not target_cur and finding_date:
        date_obj = datetime.datetime.strptime(finding_date,
                                              '%d-%m-%Y,%H:%M:%S')
        rate_value = cur_rates_obj.get_rates(currency, date_obj)

    else:
        rate_value = cur_rates_obj.get_rates(currency)

    return jsonify({
        'source_currency': currency,
        'exchange_value': rate_value,
        'status_code': 200
    })


@app.route("/convert", methods=['GET'])
def convert_currency():
    """
    The flask API for changing the currency rate from source currency to target
    currency.
    :return:
    """
    source = request.args.get('source')
    target = request.args.get('target')
    amount = request.args.get('amount')
    finding_date = request.args.get('date')

    cur_rates_obj = CurrencyRates(force_decimal=True)

    if not source or not target or not amount:
        return jsonify({
            'error': {
                'message': 'data not passed: source or target or amount.'
            },
            'status_code': 400
        })

    elif finding_date:
        date_obj = datetime.datetime.strptime(finding_date,
                                              '%d-%m-%Y,%H:%M:%S')
        value = cur_rates_obj.convert(source, target, Decimal(amount),
                                      date_obj)

    else:
        value = cur_rates_obj.convert(source, target, Decimal(amount))

    return jsonify({
        'source_currency': source,
        'target_currency': target,
        'amount': amount,
        'converted_value': value,
        'status_code': 200
    })
