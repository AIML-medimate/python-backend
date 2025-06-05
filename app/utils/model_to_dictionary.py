
def model_to_dict(obj, exclude=None):
    exclude = exclude or []
    return {
        k: v
        for k, v in obj.__dict__.items()
        if not k.startswith("_") and k not in exclude
    }

