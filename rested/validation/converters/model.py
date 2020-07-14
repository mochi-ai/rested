from django.core.exceptions import ObjectDoesNotExist


# converts a field into an orm model by looking on specified field, validation error if record doesn't exist
# usage: v.am.string.to.model
def model(model, field='id'):
    def validator(v, accept=None, reject=None):
        try:
            fields = {}
            fields[field] = v
            return model.objects.get(**fields)
        except ObjectDoesNotExist:
            reject(f'expected_model_exists')
    return validator
model.dynamic = True
