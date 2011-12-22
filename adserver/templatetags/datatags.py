from django import template
from django.db.models.fields import FieldDoesNotExist
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def data_table(queryset, display_fields):
    field_names = display_fields.split(",")
    field_headers = []
    object_list = []
    fill_field_headers = True
    for item in queryset:
        object = []
        for field_name in field_names:
            value = getattr(item, field_name)
            if callable(value):
                object.append(value())
            else:
                object.append(value)

            if fill_field_headers:
                try:
                    header = item._meta.get_field(field_name).verbose_name
                except FieldDoesNotExist:
                    header = value.short_description
                field_headers.append(header)

        fill_field_headers = False

        object_list.append(object)
    return render_to_string("datatags/data_table.html", {
        "field_headers" : field_headers,
        "object_list" : object_list,
    })
