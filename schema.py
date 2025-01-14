from marshmallow import Schema, fields

class PlainDimensionSchema(Schema):
    id = fields.Int(dump_only=True)
    stack = fields.Int(required=True)
    reach = fields.Int(required=True)
    size = fields.Str(required=True)
    seat_height = fields.Str()
    crank_length = fields.Str()

class PlainBikeSchema(Schema):
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)

class PlainProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    age =    fields.Int(required=True)
    gender = fields.Str(required=True)
    # weight = fields.Int(dump_only=True)
    # height = fields.Float(dump_only=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

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

class UserSchema(PlainUserSchema):
    profile = fields.List(fields.Nested(PlainProfileSchema), dump_only=True)

class TagSchema(PlainTagSchema):
    bike_id = fields.Int()
    bike = fields.Nested(PlainBikeSchema(), dump_only=True)
    dimensions = fields.List(fields.Nested(PlainDimensionSchema()), dump_only=True)

class TagAndDimensionSchema(Schema):
    message = fields.Str()
    dimension = fields.Nested(DimensionSchema)
    tag = fields.Nested(TagSchema)

class UserProfileSchema(PlainProfileSchema):
    user_id = fields.Int(required=True)
    user = fields.List(fields.Nested(UserSchema()), dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    tss = fields.Int(dump_only=True)
    type = fields.Str(dump_only=True)
    date = fields.DateTime(dump_only=True)
    intensity_factor = fields.Float(dump_only=True)
    kilojoules = fields.Int(dump_only=True)
    total_calories = fields.Float(dump_only=True)
    carbs = fields.Float(dump_only=True)
    protein = fields.Float(dump_only=True)
    fat = fields.Float(dump_only=True)
    api_key = fields.Str(required=True)