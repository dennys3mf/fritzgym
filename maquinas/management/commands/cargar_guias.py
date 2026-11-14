from django.core.management.base import BaseCommand
from django.db import transaction

from maquinas.catalogo import GUIAS, normalizar_nombre
from maquinas.models import Maquina


class Command(BaseCommand):
    help = 'Añade guías verificadas y completa fichas conocidas conservando sus IDs y códigos QR.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Muestra los cambios sin guardarlos.')

    @transaction.atomic
    def handle(self, *args, **options):
        existing = {normalizar_nombre(m.nombre): m for m in Maquina.objects.all()}
        created = updated = 0
        for item in GUIAS:
            machine = next((existing[normalizar_nombre(name)]
                            for name in (item['nombre'], *item['aliases'])
                            if normalizar_nombre(name) in existing), None)
            is_new = machine is None
            if is_new:
                machine = Maquina(nombre=item['nombre'])
            description = item['resumen'] + '\n\nPreparación y ejecución\n' + '\n'.join(
                f'{i}. {step}' for i, step in enumerate(item['pasos'], 1))
            description += '\n\nEvita estos errores\n' + '\n'.join(item['errores'])
            video_id = machine.youtube_id
            # Retain the existing publishers' verified demonstrations in production.
            chosen_id = video_id if video_id in item['videos_originales'] else item['video']
            fields = {'descripcion': description, 'grupo_muscular': item['grupo'],
                      'url_video': f'https://www.youtube.com/embed/{chosen_id}'}
            if not is_new and all(getattr(machine, key) == value for key, value in fields.items()):
                continue
            for key, value in fields.items():
                setattr(machine, key, value)
            machine.save()
            existing[normalizar_nombre(machine.nombre)] = machine
            created += is_new
            updated += not is_new
        if options['dry_run']:
            transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS(
            f'{"Simulación: " if options["dry_run"] else ""}{created} guías nuevas, '
            f'{updated} fichas actualizadas. No se eliminaron máquinas.'))
