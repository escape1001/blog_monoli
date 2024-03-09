from django import template

register = template.Library()

@register.simple_tag
def parse_tag_list(request):
    return request.GET.getlist('tag')

@register.simple_tag
def trans_promo_query(promotion):
    q = f"q={promotion.q}" if promotion.q else None
    tag_list = promotion.tags.values_list('name', flat=True)
    tags = ''.join(["&tag="+ tag for tag in tag_list])

    return f"?{q}{tags}"