from identity_sync.Resources.resource import Resource

class Identity(Resource):

    urls = {}

    # This method is used to ensure that we can track the biller operations are to be performed on
    def set_identity_id(self, biller_id):
        return super().set_identity_id(biller_id)

    def upload_image(self, payload=None):

        return super().read(payload=payload)

    def serialize(self, payload=None, operation=None):
        
        # Might need refractoring
        super().set_operation(operation)

        data = {}

        if operation is None:
            return "Specify the operation: Resource.UPLOAD_IMAGE"

        if operation == super().UPLOAD_IMAGE:

            # If identity_id is SMILE
            if super().get_identity_id() == super().SMILE:
                data = payload
            # If identity_id is VERIFY
            elif super().get_identity_id() == super().VERIFY:
                data.update({
                    "callback": payload.get("callback_url", ""),
                    "firstName": payload.get("first_name", ""),
                    "lastName": payload.get("last_name", ""),
                    "dob":payload.get("dob", ""),
                    "idNumber": payload.get("id_number", ""),
                    "documentNumber": payload.get("document_number", ""),
                    "type": payload.get("id_type", ""),
                    "country": payload.get("country_code", ""),
                    "vendorData": payload.get("description", ""),
                    "images": payload.get("images", "")
                })

        data.update(payload.get("additional_properties", {}))

        return data
