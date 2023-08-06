from billing_sync.Resources.resource import Resource
from billing_sync.Resources.billing import Billing

# This is the class that will be used to access the Billing resources/identities
# This is class is also a resouce on its own, it can have its own methods and functions

# Methods and functions to be used in this class are those that can be considered as 'global'
class Biller(Resource):

    _resources = {
        "Billing": Billing(),
    }

    # use the nash object to confirm if the user accessing the billers is logged in
    _nash = None

    urls = {}

    # This class is to be accessed via the Nash object, which is responsible for setting:
    # The headers and any params to be used accross all API end points
    def __init__(self, nash, biller_id=None):
        self._nash = nash
        super().__init__("BillingAPI", self._nash.get_headers(), self._nash.get_params())
        super().set_biller_id(biller_id)

    def resource(self, resource_name):
        # Get the resource
        # Set the biller (biller_id) using the resource
        # Set the resource headers, these are the headers to be used by all
        # enpoints related to the resource
        resource = self._resources[resource_name].set_biller_id(super().get_biller_id()).set_headers(self._nash.get_headers())

        return resource

    # This is a 'global' function
    # Used to get all 'resources'
    def get_resources(self):
        return list(self._resources.keys())        

    # This is a 'global' function
    # Used to get sample_payloads for a resource's end point
    def sample_payload(self, biller_id=None, payload=None):
        data = {}
        # Set the operation to be performed 
        super().set_operation(super().SAMPLE_DATA)

        # If a biller id is supplied 
        if biller_id is not None:
            # If a user did not set a biller id
            if super().get_biller_id() < 1:
                # If a user did not set a biller id, set the biller_id to the Global Biller ID 0
                super().set_biller_id(super().GLOBAL)
                # Executing the method below after setting the Global Biller ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the biller id whose sample data the user wants
                data = super().read(payload,params=f'biller_id={biller_id}')

            # If a user set a biller id
            elif super().get_biller_id() > 0:
                # Since operations are linked to a biller id, we want to get access to the Global Biller ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set biller id to
                # the user's biller ID

                # Get the user's biller id and save it temporarily (temp)
                temp = super().get_biller_id()
                # Set the biller id to the Global Biller ID
                super().set_biller_id(super().GLOBAL)

                # Execite the SAMPLE_DATA operation
                # Pass the biller id whose sample data the user wants
                data = super().read(payload,params=f'biller_id={biller_id}')

                # reset the biller_id to the biller id set by the user before (temp)
                super().set_biller_id(temp)

        # If a biller id is not supplied 
        else:
            # If a user did not set a biller id
            if super().get_biller_id() < 1:
                # If a user did not set a biller id, set the biller_id to the Global Biller ID 0
                super().set_biller_id(super().GLOBAL)         
                # Executing the method below after setting the Global Biller ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the biller id whose sample data the user wants   
                data = super().read(payload,params=f'biller_id={biller_id}')

            # If a user did set a biller id
            elif super().get_biller_id() > 0:
                # Since operations are linked to a biller id, we want to get access to the Global Biller ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set biller id to
                # the user's biller ID

                # Get the user's biller id and save it temporarily (temp)
                temp = super().get_biller_id()
                # Set the biller id to the Global Biller ID
                super().set_biller_id(super().GLOBAL)
                # Since no biller_id was passed by the user, we assume the user wants to view the sample_data
                # of the biller_id they are currently working with
                data = super().read(payload,params=f'biller_id={temp}')
                # Set biller id to back the user's orginal biller id
                super().set_biller_id(temp)
        
        # The 'if else' complexities above are done to ensure that the users can call this method
        # anywhere in their code, if they wish to get a sample data

        return data

    def callback(self, biller_name=None, payload=None, method='POST', endpoint='/callback'):

        if biller_name is not None:
            endpoint = f'{endpoint}/{biller_name}'

        return super().read(payload, method, endpoint)
    
    # This is a 'global' function
    # Used to get billers supported by Nash
    def biller_types(self,biller_id=None):

        if bool(biller_id):
            return super().read(params=f'biller_id={biller_id}')
        return super().read()
