# cerberus schema for the evaluator config
evaluator_config_schema = {
    "name": {
        "type": "string",
        "required": True,
        "check_with": "is_alphanumeric"
    },
    "description": {
        "type": "string",
        "required": True,
    },
    "author": {
        "type": "string",
        "required": True,
        "check_with": "is_author"
    },
    "creation_date": {
        "type": "datetime",
        "required": True,
    },
    "filetypes": {
        "type": "dict",
        "required": True,
    }
}
