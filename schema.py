from marshmallow import Schema, fields

class PlainDimensionSchema(Schema):
    id = fields.Int(dump_only=True)
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)
    size = fields.Str(required=True)

class PlainBikeSchema(Schema):
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class DimensionUpdateSchema(Schema):
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)
    size = fields.Str(required=True)
    bike_id = fields.Int()

class BikeUpdateSchema(Schema):
    make = fields.Str(required=True)
    model = fields.Str(required=True)

class TagUpdateSchema(Schema):
    name = fields.Str(required=True)

class DimensionSchema(PlainDimensionSchema):
    bike_id = fields.Int(required=True)
    bike = fields.Nested(PlainBikeSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class BikeSchema(PlainBikeSchema):
    dimensions = fields.List(fields.Nested(PlainDimensionSchema), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)

class TagSchema(PlainTagSchema):
    bike_id = fields.Int()
    bike = fields.Nested(PlainBikeSchema(), dump_only=True)
    dimensions = fields.List(fields.Nested(PlainDimensionSchema()), dump_only=True)

class TagAndDimensionSchema(Schema):
    message = fields.Str()
    dimension = fields.Nested(DimensionSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
