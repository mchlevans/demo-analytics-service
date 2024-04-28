from marshmallow import Schema, fields, validate

class FigureSizeSchema(Schema):
    width = fields.Int(validate=validate.Range(min=0))
    height = fields.Int(validate=validate.Range(min=0))

class PolySchema(Schema):
    size = fields.Nested(FigureSizeSchema, required=False)
    xVarName = fields.Str(required=True)
    yVarName = fields.Str(required=True)
