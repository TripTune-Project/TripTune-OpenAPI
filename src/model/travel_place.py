class TravelPlace:
    def __init__(self, location, category_code, content_type_id, place_name, address, api_content_id, api_created_at, api_updated_at,
                detail_address=None, use_time=None, check_in_time=None, check_out_time=None, homepage=None, phone_number=None, 
                longitude=None, latitude=None, description=None):
        self.location = location
        self.category_code = category_code
        self.content_type_id = content_type_id
        self.place_name = place_name
        self.address = address
        self.api_content_id = api_content_id
        self.api_created_at = api_created_at
        self.api_updated_at = api_updated_at
        self.detail_address = detail_address
        self.use_time = use_time
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.homepage = homepage
        self.phone_number = phone_number
        self.longitude = longitude
        self.latitude = latitude
        self.description = description
