# coding: utf-8
from maxipago.managers.base import ManagerTransaction, ManagerApi
from maxipago.requesters.recurring import RecurringRequester
from maxipago.resources.payment import PaymentResource
from maxipago.resources.recurring import CancelResource

class RecurringManager(ManagerTransaction):

    def add(self, **kwargs):
        fields = (
            ('processor_id', {'translated_name': 'processorID'}),
            ('reference_num', {'translated_name': 'referenceNum'}),
            ('ip_address', {'translated_name': 'ipAddress', 'required': False}),

            ('billing_name', {'translated_name': 'billing/name', 'required': False}),
            ('billing_address', {'translated_name': 'billing/address', 'required': False}),
            ('billing_address2', {'translated_name': 'billing/address2', 'required': False}),
            ('billing_city', {'translated_name': 'billing/city', 'required': False}),
            ('billing_state', {'translated_name': 'billing/state', 'required': False}),
            ('billing_postalcode', {'translated_name': 'billing/postalcode', 'required': False}),
            ('billing_country', {'translated_name': 'billing/country', 'required': False}),
            ('billing_phone', {'translated_name': 'billing/phone', 'required': False}),
            ('billing_email', {'translated_name': 'billing/email', 'required': False}),

            ('shipping_name', {'translated_name': 'shipping/name', 'required': False}),
            ('shipping_address', {'translated_name': 'shipping/address', 'required': False}),
            ('shipping_address2', {'translated_name': 'shipping/address2', 'required': False}),
            ('shipping_city', {'translated_name': 'shipping/city', 'required': False}),
            ('shipping_state', {'translated_name': 'shipping/state', 'required': False}),
            ('shipping_postalcode', {'translated_name': 'shipping/postalcode', 'required': False}),
            ('shipping_country', {'translated_name': 'shipping/country', 'required': False}),
            ('shipping_phone', {'translated_name': 'shipping/phone', 'required': False}),
            ('shipping_email', {'translated_name': 'shipping/email', 'required': False}),

            ('card_number', {'translated_name': 'transactionDetail/payType/creditCard/number', 'required': False}),
            ('card_expiration_month', {'translated_name': 'transactionDetail/payType/creditCard/expMonth', 'required': False}),
            ('card_expiration_year', {'translated_name': 'transactionDetail/payType/creditCard/expYear', 'required': False}),
            ('card_cvv', {'translated_name': 'transactionDetail/payType/creditCard/cvvNumber', 'required': False}),

            ('charge_total', {'translated_name': 'payment/chargeTotal'}),
            ('currency_code', {'translated_name': 'payment/currencyCode', 'required': True}),

            ('recurring_action', {'translated_name': 'recurring/action', 'default': 'new'}),
            ('recurring_start', {'translated_name': 'recurring/startDate', 'required': False}),
            ('recurring_last', {'translated_name': 'recurring/lastDate', 'required': False}),
            ('recurring_next_fire', {'translated_name': 'recurring/nextFireDate', 'required': False}),
            ('recurring_fire_day', {'translated_name': 'recurring/fireDay', 'required': False}),
            ('recurring_frequency', {'translated_name': 'recurring/frequency'}),
            ('recurring_period', {'translated_name': 'recurring/period'}),
            ('recurring_first_amount', {'translated_name': 'recurring/firstAmount', 'required': False}),
            ('recurring_last_amount', {'translated_name': 'recurring/lastAmount', 'required': False}),
            ('recurring_installments', {'translated_name': 'recurring/installments'}),
            ('recurring_failure_threshold', {'translated_name': 'recurring/failureThreshold', 'required': False}),
        )
        requester = RecurringRequester(fields, kwargs)
        resource = PaymentResource
        return self.send(command='recurringPayment', requester=requester, resource=resource)


    def delete(self, **kwargs):
        fields = (
            ('order_id', {'translated_name': 'orderID'}),
        )

        requester = RecurringRequester(fields, kwargs)
        
        manager = ManagerApi(maxid=self.maxid, api_key=self.api_key, api_version=self.api_version, sandbox=self.sandbox)
        return manager.send(command='cancel-recurring', requester=requester, resource=CancelResource)
