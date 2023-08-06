from identity_sync.Resources.resource import Resource
from identity_sync.Resources.identity import Identity


class KYC(Resource):

    _resources = {
        "Identity": Identity(),
    }

    # use the nash object to confirm if the user accessing the identities is logged in
    _nash = None

    urls = {}

    def __init__(self, nash, identity_id=None):
        self._nash = nash
        super().__init__("IdentityAPI", self._nash.get_headers(), self._nash.get_params())
        super().set_identity_id(identity_id)

    def resource(self, resource_name):
        resource = self._resources[resource_name].set_identity_id(
            super().get_identity_id()).set_headers(self._nash.get_headers())

        return resource

    def get_resources(self):
        return list(self._resources.keys())        

    # def sample_payload(self, identity_id=None, payload = None, method='GET',endpoint="/sample_payload"):

    #     if identity_id is not None:
    #         endpoint = f'{endpoint}/{identity_id}'

    #     return super().read(payload, method, endpoint)

    # def identity_types(self, identity_id=None, payload = None, method='GET',endpoint="/identity_types"):

    #     if identity_id is not None:
    #         endpoint = f'{endpoint}/{identity_id}'

    #     return super().read(payload, method, endpoint)
    
    # This is a 'global' function
    # Used to get identities supported by Nash
    # def identity_types(self,identity_id=None):

    #     if bool(identity_id):
    #         return super().read(params=f'identity_id={identity_id}')
    #     return super().read()
    
    # This is a 'global' function
    # Used to get identities supported by Nash
    def identity_types(self,identity_id=None):
        return self.exec_global_function(operation=super().KYC_IDENTITIES, identity_id=identity_id)      

    # This is a 'global' function
    # Used to get sample_payloads for a resource's end point
    def sample_payload(self, identity_id=None, payload=None):
        return self.exec_global_function(operation=super().SAMPLE_DATA, identity_id=identity_id, payload=payload)

    # This method is responsible for returning the identity id that's to execute the 'global' functions
    def exec_global_function(self, operation = 0, identity_id=None, payload=None):
        data = {}
        # Set the operation to be performed 
        super().set_operation(operation)

        # If a identity id is supplied 
        if identity_id is not None:
            # If a user did not set a identity id
            if super().get_identity_id() < 1:
                # If a user did not set a identity id, set the identity_id to the Global Identity ID 0
                super().set_identity_id(super().GLOBAL)
                # Executing the method below after setting the Global Identity ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the identity id whose sample data the user wants
                data = super().read(payload,params=f'identity_id={identity_id}')

            # If a user set a identity id
            elif super().get_identity_id() > 0:
                # Since operations are linked to a identity id, we want to get access to the Global Identity ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set identity id to
                # the user's identity ID

                # Get the user's identity id and save it temporarily (temp)
                temp = super().get_identity_id()
                # Set the identity id to the Global Identity ID
                super().set_identity_id(super().GLOBAL)

                # Execite the SAMPLE_DATA operation
                # Pass the identity id whose sample data the user wants
                data = super().read(payload,params=f'identity_id={identity_id}')

                # reset the identity_id to the identity id set by the user before (temp)
                super().set_identity_id(temp)

        # If a identity id is not supplied 
        else:
            # If a user did not set a identity id
            if super().get_identity_id() < 1:
                # If a user did not set a identity id, set the identity_id to the Global Identity ID 0
                super().set_identity_id(super().GLOBAL)         
                # Executing the method below after setting the Global Identity ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the identity id whose sample data the user wants   
                data = super().read(payload,params=f'identity_id={identity_id}')

            # If a user did set a identity id
            elif super().get_identity_id() > 0:
                # Since operations are linked to a identity id, we want to get access to the Global Identity ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set identity id to
                # the user's identity ID

                # Get the user's identity id and save it temporarily (temp)
                temp = super().get_identity_id()
                # Set the identity id to the Global Identity ID
                super().set_identity_id(super().GLOBAL)

                # Execite the SAMPLE_DATA operation
                # Pass the identity id whose sample data the user wants
                data = super().read(payload,params=f'identity_id={identity_id}')
                # Set identity id to back the user's orginal identity id
                super().set_identity_id(temp)
        
        # The 'if else' complexities above are done to ensure that the users can call this method
        # anywhere in their code, if they wish to get a sample data

        return data