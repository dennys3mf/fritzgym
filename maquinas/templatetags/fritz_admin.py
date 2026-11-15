from django import template
from django.db.models import Count

from maquinas.models import Anuncio, Maquina

register = template.Library()


@register.simple_tag(takes_context=True)
def fritz_overview(context):
    user = context.get('user')
    if not user or not user.is_active or not user.is_staff:
        return {}
    result = {}
    if user.has_perm('maquinas.view_maquina') or user.has_perm('maquinas.change_maquina'):
        counts = dict(Maquina.objects.values_list('grupo_muscular').annotate(total=Count('id')))
        result.update(machines=sum(counts.values()), groups=sum(count > 0 for count in counts.values()),
                      group_rows=[{'code': code, 'name': name, 'count': counts.get(code, 0)}
                                  for code, name in Maquina.GrupoMuscular.choices])
    if user.has_perm('maquinas.view_anuncio') or user.has_perm('maquinas.change_anuncio'):
        result['active_announcements'] = Anuncio.objects.filter(activo=True).count()
        result['hidden_announcements'] = Anuncio.objects.filter(activo=False).count()
    return result
