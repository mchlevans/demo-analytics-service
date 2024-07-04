from marshmallow import Schema, fields, validate

class PolySchema(Schema):
    xVarNames = fields.List(fields.Str, required=True)
    yVarName = fields.Str(required=True)
    polynomial = fields.Int(required=True)
    width = fields.Int(validate=validate.Range(min=1), required=False)
