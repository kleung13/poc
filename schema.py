from marshmallow import Schema, fields

class DimensionSchema(Schema):
    dimension_id = fields.Str()
    bike_id = fields.Str(required=True)
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)

class DimensionUpdateSchema(Schema):
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)

class BikeSchema(Schema):
    bike_id = fields.Str(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)

class BikeUpdateSchema(Schema):
    make = fields.Str(required=True)
    model = fields.Str(required=True)