from marshmallow import Schema, fields

class PlainDimensionSchema(Schema):
    id = fields.Str()
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)
    size = fields.Str(required=True)

class PlainBikeSchema(Schema):
    id = fields.Str(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)

class DimensionUpdateSchema(Schema):
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)
    size = fields.Str(required=True)
    bike_id = fields.Int()

class BikeUpdateSchema(Schema):
    make = fields.Int(required=True)
    model = fields.Int(required=True)

class DimensionSchema(PlainDimensionSchema):
    bike_id = fields.Int(required=True)
    bike = fields.Nested(PlainBikeSchema(), dump_only=True)

class BikeSchema(PlainBikeSchema):
    dimensions = fields.List(fields.Nested(PlainDimensionSchema), dump_only=True)