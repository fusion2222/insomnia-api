from settings import APP
import requests

from views import BalanceView, HelathCheckView


APP.add_url_rule(
    '/hc',
    view_func=HelathCheckView.as_view('health_check')
)
APP.add_url_rule(
    '/<string:account_address>',
    view_func=BalanceView.as_view('balance')
)
