# cerberus schema for the evaluator config
evaluator_config_schema = {
    "name": {
        "type": "string",
        "required": True,
        "check_with": "is_alphanumeric"
    },
    "description": {
        "type": "string",
        "required": True
    },
    "author": {
        "type": "string",
        "required": True,
        "check_with": "is_author"
    },
    "creation_date": {
        "type": "datetime",
        "required": True
    },
    "filetypes": {
        "type": "dict",
        "valueschema": {
            "type": "dict",
            "schema": {
                "filetype": {
                    "type": "string",
                    "check_with": "is_alphanumeric"
                },
                "kwargs": {
                    "type": "dict"
                },
                "extractors": {
                    "type": "list",
                    "schema": {
                        "type": "dict"
                    }
                },
                "transformers": {
                    "type": "list",
                    "schema": {
                        "type": "dict"
                    }
                },
                "reporters": {
                    "type": "list",
                    "schema": {
                        "type": "dict"
                    }
                },
                "reportaggregators": {
                    "type": "list",
                    "schema": {
                        "type": "dict"
                    }
                }
            }
        }
    }
}
