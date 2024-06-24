from marshmallow import Schema, fields, validate

# class FigureSizeSchema(Schema):
#     width = fields.Int(validate=validate.Range(min=0))

class PolySchema(Schema):
    # size = fields.Nested(FigureSizeSchema, required=False)
    xVarNames = fields.List(fields.Str, required=True)
    yVarName = fields.Str(required=True)
    polynomial = fields.Int(required=True)
    width = fields.Int(validate=validate.Range(min=1), required=False)
