class Operations(object):


    # These are the billing integrations
    # Each with a unique ID
    GLOBAL = 0
    IPAY = 1
    FLUTTERWAVE = 2
    TINGG = 3

    # These are the operations to be performed in Billing Identity
    # Each with a unique incremental ID

    # Returns Sample Data
    SAMPLE_DATA = -1
    # Returns a list of supported billers by Nash
    BILLERS = SAMPLE_DATA + 1
    # Returns a list of supported billers by Nash
    SUPPORTED_BILLERS = BILLERS + 1
    # Returns the balance in the configured billing account
    BALANCE = SUPPORTED_BILLERS + 1
    # Checks if the biller's connection/network is up/down
    BILLER_STATUS = BALANCE + 1
    # Returns the network provider using a mobile number's prefix
    NUMBER_LOOK_UP = BILLER_STATUS + 1
    # Returns the status of a transaction
    TRANSACTION_STATUS = NUMBER_LOOK_UP + 1
    # Executes a bill payment
    BILL_PAYMENT = TRANSACTION_STATUS + 1
    # Returns the bills filtered by country
    BILL_BY_COUNTRY = BILL_PAYMENT + 1
    # Returns the bills filtered by provider
    BILL_BY_PROVIDER = BILL_BY_COUNTRY + 1
    # Confirms if a client's/customer's blling account is valid
    VALIDATE_CUSTOMER = BILL_BY_PROVIDER + 1
    # Returns a generated OTP
    GENERATE_OTP = VALIDATE_CUSTOMER + 1
    # Validates a generated OTP
    VALIDATE_OTP = GENERATE_OTP + 1
    # Queries a bill
    QUERY_BILL = VALIDATE_OTP + 1


    # All end points are placed in the BILLERS_CONF 
    # This is to allow easy standardization of the base url, endpoint and operations
    # When calling the APIs, in this case this is done in the read function
    BILLERS_CONF = {
        GLOBAL: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/billing",
                "operations": {
                    SAMPLE_DATA: ("sample_payload", "POST"),
                    BILLERS: ("billers", "GET"),
                }
            }

        },
        IPAY: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/billing/{IPAY}",
                "operations": {
                    SUPPORTED_BILLERS: ("get_billers", "GET"),
                    BILLER_STATUS: ("get_biller_status", "POST"),
                    NUMBER_LOOK_UP: ("get_number_look_up", "POST"),
                    BALANCE: ("get_account_balance", "POST"),
                    VALIDATE_CUSTOMER: ("validate_bill_account", "POST"),
                    BILL_PAYMENT: ("make_bill_payment", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        TINGG: {
            "url": "https://dev.billingservices.nashglobal.co",
            "read": {
                "endpoint": "api/Tingg",
                "operations": {
                    BILL_PAYMENT: ("create_bill", "POST"),
                    QUERY_BILL: ("query_bill", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        FLUTTERWAVE: {
            "url": "https://dev.billingservices.nashglobal.co",
            "read": {
                "endpoint": "api/Flutterwave",
                "operations": {
                    BILL_BY_COUNTRY: ("get_bills_by_country", "GET"),
                    BILL_BY_PROVIDER: ("get_bills_by_provider", "GET"),
                    BILL_PAYMENT: ("create_bill", "POST"),
                    VALIDATE_CUSTOMER: ("validate_customer_details", "GET"),
                    TRANSACTION_STATUS: ("get_transaction_status", "GET"),
                    GENERATE_OTP: ("generate_otp", "POST"),
                    VALIDATE_OTP: ("validate_otp", "POST"),
                }
            }

        }
    }