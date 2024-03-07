from django import template

register = template.Library()

@register.simple_tag
def parse_tag_list(request):
    return request.GET.getlist('tag')