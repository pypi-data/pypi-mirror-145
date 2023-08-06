class Operations(object):


    # These are the identity integrations
    # Each with a unique ID
    GLOBAL = 0
    SMILE = 1
    VERIFY = 2

    # These are the operations to be performed in Billing Identity
    # Each with a unique incremental ID

    # Returns Sample Data
    SAMPLE_DATA = -1
    # Returns a list of supported billers by Nash
    KYC_IDENTITIES = SAMPLE_DATA + 1
    # Returns a list of supported billers by Nash
    UPLOAD_IMAGE = KYC_IDENTITIES + 1


    # All end points are placed in the BILLERS_CONF 
    # This is to allow easy standardization of the base url, endpoint and operations
    # When calling the APIs, in this case this is done in the read function
    KYC_CONF = {
        GLOBAL: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/kyc",
                "operations": {
                    SAMPLE_DATA: ("sample_payload", "POST"),
                    KYC_IDENTITIES: ("identity_types", "GET"),
                }
            }

        },
        SMILE: {
            "url": "http://127.0.0.1:8000",
            "read": {
                "endpoint": f"api/kyc/smileidentity",
                "operations": {
                    UPLOAD_IMAGE: ("upload_image", "POST"),
                }
            }

        },
        VERIFY: {
            "url": "http://20.23.47.36",
            "read": {
                "endpoint": f"api/kyc/veriff",
                "operations": {
                    UPLOAD_IMAGE: ("upload_image", "POST"),
                }
            }

        }
    }