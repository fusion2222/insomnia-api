from json.decoder import JSONDecodeError

import requests
from flask import request, url_for
from flask.views import View

import settings
from utils import err_response, absolute_url


class BalanceView(View):
    methods = ['GET']
    
    def dispatch_request(self, account_address):        
        if request.headers.get('Authorization', '') != settings.API_KEY:
            return err_response(
                "Incorrect API key. Example auth HTTP header - Authorization : XXXX", 403
            )
        
        try:
            response = requests.get(
                f'{settings.TRX_ACCOUNT_BALANCE_URI}{account_address}',
                timeout=settings.TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            return err_response("Gateway Timeout Error", 504)
        try:
            if response.status_code != 200:
                return response.json(), response.status_code
            
            return {
                'success': True,
                'balance': response.json()['data'][0]['balance']
            }, 200

        except (JSONDecodeError, IndexError, KeyError) as e:
            return err_response("Gateway response is not a valid JSON", 502)


class HelathCheckView(View):
    methods = ['GET']

    def check_connectivity(self):
        try:
            requests.head(
                f'{settings.TRX_ACCOUNT_BALANCE_URI}',
                timeout=settings.TIMEOUT
            )
            return True
        except requests.exceptions.ConnectionError:
            return False

    def check_balance_without_token(self):
        balance_endpoint_uri = absolute_url('balance', account_address='xxx')
        
        try:
            response = requests.get(
                balance_endpoint_uri, timeout=settings.TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            return False
        
        return response.status_code == 403

    def check_balance_with_incorrect_token(self):
        balance_endpoint_uri = absolute_url('balance', account_address='xxx')
        
        try:
            response = requests.get(
                balance_endpoint_uri,
                timeout=settings.TIMEOUT,
                headers={'Authorization': settings.API_KEY + 'xxx'}
            )
        except requests.exceptions.ConnectionError:
            return False
        
        return response.status_code == 403

    def check_balance_with_correct_token(self):
        balance_endpoint_uri = absolute_url('balance', account_address='xxx')
        
        try:
            response = requests.get(
                balance_endpoint_uri,
                timeout=settings.TIMEOUT,
                headers={'Authorization': settings.API_KEY}
            )
        except requests.exceptions.ConnectionError:
            return False
        
        return response.status_code != 403

    def dispatch_request(self):
        """
        Simple healthcheck inspects following:
        - Connectivity to 3rd party API
        - Access to balance endpoint if auth token is not provided
        - Access to balance endpoint if auth token is provided but incorrect
        - Access to balance endpoint if auth token is provided and is correct
        """

        connectivity = self.check_connectivity()
        token_authentication = self.check_balance_without_token()
        token_validity = self.check_balance_with_incorrect_token() and self.check_balance_with_correct_token()

        return {
            "connectivity": connectivity,
            "token_authentication": token_authentication,
            "token_validity": token_validity
        }, 200
    