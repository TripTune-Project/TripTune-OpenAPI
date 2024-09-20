class TravelPlace:
    # def __init__(self, country_id, city_id, district_id, category_code, content_type_id, place_name, address, detail_address,
    #              longitude, latitude, api_content_id, api_created_at, api_updated_at):
    #     self.country_id = country_id
    #     self.city_id = city_id
    #     self.district_id = district_id
    #     self.category_code = category_code
    #     self.content_type_id = content_type_id
    #     self.place_name = place_name
    #     self.address = address
    #     self.detail_address = detail_address
    #     self.longitude = longitude
    #     self.latitude = latitude
    #     self.api_content_id = api_content_id
    #     self.api_created_at = api_created_at
    #     self.api_updated_at = api_updated_at

    def __init__(self, location, category_code, content_type_id, place_name, address, detail_address,
                 longitude, latitude, api_content_id, api_created_at, api_updated_at):
        self.location = location
        self.category_code = category_code
        self.content_type_id = content_type_id
        self.place_name = place_name
        self.address = address
        self.detail_address = detail_address
        self.longitude = longitude
        self.latitude = latitude
        self.api_content_id = api_content_id
        self.api_created_at = api_created_at
        self.api_updated_at = api_updated_at

    

