from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def data_table(queryset, display_fields):
    field_names = display_fields.split(",")
    model_fields = queryset.model._meta.fields
    fields = [field for field in model_fields if field.name in field_names]
    object_list = []
    for item in queryset:
        object = {}
        for field_name in field_names:
            object[field_name] = getattr(item, field_name)
        object_list.append(object)
    return render_to_string("datatags/data_table.html", {
        "fields" : fields,
        "object_list" : object_list,
    })
