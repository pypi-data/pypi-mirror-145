from billing_sync.Resources.resource import Resource
from datetime import datetime

class Billing(Resource):

    urls = {}

    # This method is used to ensure that we can track the biller operations are to be performed on
    def set_biller_id(self, biller_id):
        return super().set_biller_id(biller_id)

    def balance(self, payload=None):

        return super().read(payload=payload)

    def number_look_up(self, payload=None):

        return super().read(payload=payload)

    def bill_payment(self, payload=None):

        return super().read(payload=payload)

    def biller_status(self, payload=None):

        return super().read(payload=payload)

    def get_billers(self, payload=None):

        return super().read(payload=payload)

    def transaction_status(self, payload=None):

        return super().read(payload=payload, params=f'reference={payload.get("reference","")}')

    def bills_by_country(self, payload=None):
        
        return super().read(payload=payload, params=f'countryCode={payload.get("countryCode","")}')

    def bills_by_provider(self, payload=None):

        return super().read(payload=payload, params=f'billerCode={payload.get("billerCode","")}')

    def validate_customer(self, payload=None):

        return super().read(payload=payload, params=f'billerCode={payload.get("billerCode","")}&itemCode={payload.get("itemCode","")}&customerIdentifier={payload.get("customerIdentifier","")}')

    def generate_otp(self, payload=None):

        return super().read(payload=payload)

    def validate_otp(self, payload=None):

        return super().read(payload=payload)

    def query_bill(self, payload=None):

        return super().read(payload=payload)

    def serialize(self, payload=None, operation=None):

        super().set_operation(operation)

        data = {}

        if operation is None:
            raise Exception("Specify the operation: Resource.BALANCE, Resource.NUMBER_LOOK_UP, Resource.VALIDATE_CUSTOMER, Resource.BILL_PAYMENT, Resource.BILL_BY_COUNTRY, Resource.BILL_BY_PROVIDER, Resource.QUERY_BILL, Resource.GENERATE_OTP, Resource.VALIDATE_OTP or Resource.TRANSACTION_STATUS")

        if operation == super().BALANCE:

            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                pass

        elif operation == super().NUMBER_LOOK_UP:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                data.update({
                    "prefix": payload.get("prefix", ""),
                    })

        elif operation == super().BILL_BY_COUNTRY:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                data["countryCode"] = payload.get("country_code", "")

        elif operation == super().BILL_BY_PROVIDER:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                data["billerCode"] = payload.get("biller_code", "")

        elif operation == super().QUERY_BILL:
            # If biller_id is IPAY
            if super().get_biller_id() == super().TINGG:
                data.update({
                    "countryCode": payload.get("country_code", ""),
                    "serviceCode": payload.get("service_code", ""),
                    "msisdn": payload.get("phone_number", ""),
                    "accountNumber": payload.get("account_number", ""),
                    "payerTransactionID": payload.get("payer_transaction_id", ""),
                    "callbackUrl": payload.get("callback_url", ""),
                })

        elif operation == super().VALIDATE_CUSTOMER:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                data.update({
                    "billerCode": payload.get("biller_code", ""),
                    "itemCode": payload.get("item_code", ""),
                    "customerIdentifier": payload.get("customer_id", ""),
                    })
            # If biller_id is IPAY
            elif super().get_biller_id() == super().IPAY:
                data.update({
                    "account_type": payload.get("biller_code", ""),
                    "account": payload.get("customer_id", ""),
                    })

        elif operation == super().GENERATE_OTP:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                data.update({
                    "name": payload.get("name", ""),
                    "email": payload.get("email", ""),
                    "phone": payload.get("phone", "")
                })

        elif operation == super().BILLER_STATUS:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                data.update({
                    "biller_code": payload.get("biller_code", ""),
                })

        elif operation == super().VALIDATE_OTP:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                data.update({
                    "otp": payload.get("otp", ""),
                    "ref": payload.get("reference", ""),
                })

        elif operation == super().BILL_PAYMENT:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                data.update({
                    "biller_name": payload.get("biller_code", ""),
                    "amount": f'{payload.get("amount", 0)}',
                    "account": payload.get("account_number", ""),
                    "phone": payload.get("phone_number", ""),
                    "merchant_reference": payload.get("reference", ""),
                })
            # If biller_id is IPAY
            elif super().get_biller_id() == super().FLUTTERWAVE:
                data.update({
                    "country": payload.get("country_code", ""),
                    "customerIdentifier": payload.get("account_number", ""),
                    "amount": payload.get("amount", 0),
                    "billType": payload.get("biller_code", ""),
                    "referenceCode": payload.get("reference", ""),
                    })
            # If biller_id is IPAY
            elif super().get_biller_id() == super().TINGG:
                data.update({
                    "countryCode": payload.get("country_code", ""),
                    "serviceCode": payload.get("biller_code", ""),
                    "msisdn": payload.get("phone_number", ""),
                    "invoiceNumber": payload.get("invoice_number", ""),
                    "accountNumber": payload.get("account_number", ""),
                    "payerTransactionID": payload.get("reference", ""),
                    "amount": payload.get("amount", 0),
                    "narration": payload.get("narration", ""),
                    "datePaymentReceived": payload.get("date_payment_received", ""),
                    "callbackUrl": payload.get("callback_url", ""),
                    "currencyCode": payload.get("currency_code", ""),
                    "customerNames": payload.get("customer_names", ""),
                    "paymentMode": payload.get("payment_mode", ""),
                })

        elif operation == super().TRANSACTION_STATUS:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                data.update({
                    "reference": f'{payload.get("reference", "")}'
                })
            # If biller_id is FLUTTERWAVE
            elif super().get_biller_id() == super().FLUTTERWAVE:
                data.update({
                    "reference": f'{payload.get("reference", "")}'
                })
            # If biller_id is TINGG
            elif super().get_biller_id() == super().TINGG:
                data.update({
                    "countryCode": payload.get("country_code", ""),
                    "payerTransactionID": payload.get("reference", ""),
                    "beepTransactionID": payload.get("beep_transaction_id", ""),
                    "clientCode": payload.get("client_code", ""),
                    "callbackUrl": payload.get("callback_url", "")
                })
            
        data.update(payload.get("additional_properties", {}))

        return data

    def response(self):

        data = {}

        response_data = super().response()

        if super().get_operation() == super().TRANSACTION_STATUS:

            if super().get_biller_id() == super().TINGG:

                if response_data.get("status") == 'error':
                    data["code"] = 0
                else:
                    data["code"] = 1
                    data["data"] = {
                        "biller_name": response_data.get("data", [{}])[0].get("serviceName"),
                        "account": response_data.get("data", [{}])[0].get("accountNumber"),
                        "phone": response_data.get("data", [{}])[0].get("MSISDN"),
                        "amount": response_data.get("data", [{}])[0].get("amount"),
                        "date": response_data.get("data", [{}])[0].get("dateCreated"),
                        "reference": response_data.get("data", [{}])[0].get("payerTransactionID"),
                    }
                data["message"] = response_data.get("message", "")

            elif super().get_biller_id() == super().IPAY:

                if response_data.get("msg", {}).get("status") == 0:
                    data["code"] = 0
                    data["message"] = response_data.get("msg", {}).get("text")

                elif response_data.get("msg", {}).get("status") == 1:
                    data["code"] = 1
                    data["message"] = response_data.get("msg", {}).get("text", {}).get("transaction_message")
                    data["data"] = {
                        "biller_name": response_data.get("msg", {}).get("text", {}).get("biller_name"),
                        "account": response_data.get("msg", {}).get("text", {}).get("account"),
                        "phone": response_data.get("msg", {}).get("text", {}).get("phone"),
                        "amount": float(response_data.get("msg", {}).get("text", {}).get("amount")),
                        "date": response_data.get("msg", {}).get("text", {}).get("biller_response_time"),
                        "reference": response_data.get("msg", {}).get("text", {}).get("biller_reference"),
                    }

            elif super().get_biller_id() == super().FLUTTERWAVE:

                if response_data.get("status") == 'error':
                    data["code"] = 0
                else:
                    data["code"] = 1
                    data["data"] = response_data.get("data")
                data["message"] = response_data.get("message", "")

        elif super().get_operation() == super().BILL_PAYMENT:
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["code"] = 0
                    data["message"] = response_data.get("error", [{}])

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("msg", {}).get("text", "")
                    data["transaction_id"] = response_data.get("msg", [{}]).get("ipay_reference")

            elif super().get_biller_id() == super().TINGG:
                if response_data.get("status", "") == "success":
                    data["code"] = 1
                    data["message"] = response_data.get("data", [{}])[0].get("statusDescription")
                    data["transaction_id"] = response_data.get("data", [{}])[0].get("payerTransactionID")
                else:
                    data["code"] = 0
                    data["message"] = response_data.get("message")
                    
            elif super().get_biller_id() == super().FLUTTERWAVE:
                if response_data.get("status") == 'error':
                    data["code"] = 0
                else:
                    data["code"] = 1
                    data["data"] = response_data.get("data")
                data["message"] = response_data.get("message", "")

        elif super().get_operation() == super().VALIDATE_CUSTOMER:
            # Standardize IPAY
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["code"] = 0
                    data["message"] = response_data.get("text", "")

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("text", "")

            # Standardize Flutterwave
            elif super().get_biller_id() == super().FLUTTERWAVE:
                if response_data.get("status") == 'error':
                    data["code"] = 0
                else:
                    data["code"] = 1
                data["message"] = response_data.get("message", "")

        elif super().get_operation() == super().BILLER_STATUS:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["code"] = 0
                    data["message"] = response_data.get("error", {}).get("text", "")

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("data", {}).get("status", "")

        elif super().get_operation() == super().BALANCE:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["response_data"] = response_data
                    data["code"] = 0
                    # data["message"] = response_data.get("error", {}).get("text", "")

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("balance", "")

        elif super().get_operation() == super().NUMBER_LOOK_UP:
            # If biller_id is IPAY
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["code"] = 0
                    data["message"] = response_data.get("text", "")

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("data", {}).get("operator", "")

        elif super().get_operation() == super().BILL_BY_COUNTRY or super().get_operation() == super().BILL_BY_PROVIDER:
            # If biller_id is FLUTTERWAVE
            if super().get_biller_id() == super().FLUTTERWAVE:
                if response_data.get("status") == 'error':
                    data["code"] = 0
                    data["message"] = response_data.get("message", "")

                elif response_data.get("status") == 'success':
                    data["code"] = 1
                    data["message"] = response_data.get("message", "")
                    data["data"] = response_data.get("data", [])
                    for i in range(len(data["data"])):
                        if 'country' in data["data"][i].keys():
                            data["data"][i]['country_code'] = data["data"][i].pop('country')

        elif super().get_operation() == super().GENERATE_OTP:
            # If biller_id is IPAY
            if super().get_biller_id() == super().FLUTTERWAVE:
                if response_data.get("status") != 'success':
                    data["code"] = 0
                    data["message"] = response_data.get("title", "")

                elif response_data.get("status") == 'success':
                    data["code"] = 1
                    data["message"] = response_data.get("message", "")
                    data["data"] = response_data.get("data", [])
                    for i in range(len(data["data"])):
                        if 'expiry' in data["data"][i].keys():
                            data["data"][i]['expiry'],_=data["data"][i]['expiry'].split('.')

        elif super().get_operation() == super().VALIDATE_OTP:
            # If biller_id is FLUTTERWAVE
            if super().get_biller_id() == super().FLUTTERWAVE:
                if response_data.get("status") != 'success':
                    data["code"] = 0
                    data["message"] = response_data.get("message", "")

                elif response_data.get("status") == 'success':
                    data["code"] = 1
                    data["message"] = response_data.get("message", "")

        elif super().get_operation() == super().SUPPORTED_BILLERS:
            # If biller_id is FLUTTERWAVE
            if super().get_biller_id() == super().IPAY:
                if response_data.get("header_status", 0) != 200:
                    data["code"] = 0
                    data["message"] = response_data.get("text", "")

                elif response_data.get("header_status", 0) == 200:
                    data["code"] = 1
                    data["message"] = response_data.get("data", [{}])

        elif super().get_operation() == super().QUERY_BILL:
            # If biller_id is IPAY
            if super().get_biller_id() == super().TINGG:
                if response_data.get("status") != 'success':
                    data["code"] = 0
                    data["message"] = response_data.get("message", "")

                elif response_data.get("status") == 'success':
                    data["code"] = 1
                    data["message"] = response_data.get("message", "")
                    data["data"] = response_data.get("data", [])
                    for i in range(len(data["data"])):
                        if 'accountNumber' in data["data"][i].keys():
                            data["data"][i]['account_number'] = data["data"][i].pop('accountNumber')
                        if 'serviceID' in data["data"][i].keys():
                            data["data"][i]['service_id'] = data["data"][i].pop('serviceID')
                        if 'serviceCode' in data["data"][i].keys():
                            data["data"][i]['service_code'] = data["data"][i].pop('serviceCode')
                        if 'dueDate' in data["data"][i].keys():
                            data["data"][i]['due_date'] = data["data"][i].pop('dueDate')
                        if 'dueAmount' in data["data"][i].keys():
                            data["data"][i]['due_amount'] = data["data"][i].pop('dueAmount')
                        if 'currency' in data["data"][i].keys():
                            data["data"][i]['currency_code'] = data["data"][i].pop('currency')
                        if 'customerName' in data["data"][i].keys():
                            data["data"][i]['customer_name'] = data["data"][i].pop('customerName')
                        if 'responseExtraData' in data["data"][i].keys():
                            data["data"][i]['extra_data'] = data["data"][i].pop('responseExtraData')
                        if 'statusCode' in data["data"][i].keys():
                            data["data"][i]['status_code'] = data["data"][i].pop('statusCode')
                        if 'statusDescription' in data["data"][i].keys():
                            data["data"][i]['description'] = data["data"][i].pop('statusDescription')

        if bool(data):
            return data

        return super().response()
