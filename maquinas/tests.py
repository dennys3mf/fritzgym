from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.management import call_command
from io import StringIO

from .models import Anuncio, Maquina
from .catalogo import GUIAS, obtener_guia


TEST_STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}


@override_settings(STORAGES=TEST_STORAGES)
class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.leg = Maquina.objects.create(
            nombre='Prensa A&B', descripcion='Trabajo de piernas',
            grupo_muscular='PI', url_video='https://www.youtube.com/embed/46Ae9zoLEcg',
        )
        cls.chest = Maquina.objects.create(
            nombre='Press de pecho', descripcion='Trabajo de pectorales',
            grupo_muscular='PE', url_video='https://www.youtube.com/embed/46Ae9zoLEcg',
        )

    def test_public_routes_and_missing_machine(self):
        for name in ['lista-maquinas', 'contacto', 'sobre-nosotros', 'privacidad']:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertEqual(self.client.get(reverse('detalle-maquina', args=[9999])).status_code, 404)

    def test_search_and_group_combine_without_losing_query(self):
        response = self.client.get(reverse('lista-maquinas'), {'q': 'A&B', 'grupo': 'PI'})
        self.assertQuerySetEqual(response.context['maquinas_list'], [self.leg])
        self.assertContains(response, 'q=A%26B')
        response = self.client.get(reverse('lista-maquinas'), {'q': 'Prensa', 'grupo': 'PE'})
        self.assertQuerySetEqual(response.context['maquinas_list'], [])
        self.assertContains(response, 'No encontramos esa máquina.')

    def test_active_announcements_and_external_link(self):
        Anuncio.objects.create(titulo='Aviso visible', contenido='Información de sala', activo=True,
                               enlace_opcional='https://example.com/aviso')
        Anuncio.objects.create(titulo='Aviso oculto', contenido='Borrador', activo=False)
        response = self.client.get(reverse('lista-maquinas'))
        self.assertContains(response, 'Aviso visible')
        self.assertNotContains(response, 'Aviso oculto')
        self.assertContains(response, 'https://example.com/aviso')

    def test_detail_preserves_tutorial_description_and_timer_controls(self):
        response = self.client.get(reverse('detalle-maquina', args=[self.leg.id]))
        for text in [self.leg.url_video, self.leg.descripcion, 'timerDisplay', 'startTimerBtn',
                     'resetTimerBtn', 'data-time="180"', 'role="status"']:
            self.assertContains(response, text)

    def test_qr_remains_a_png(self):
        response = self.client.get(reverse('generar-qr', args=[self.leg.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertTrue(response.content.startswith(b'\x89PNG\r\n\x1a\n'))


@override_settings(STORAGES=TEST_STORAGES)
class GuideContentTests(TestCase):
    def test_content_command_preserves_production_records_and_qr_ids(self):
        original = Maquina.objects.create(
            id=67, nombre='Aperturas en máquina', descripcion='Descripción inicial',
            grupo_muscular='PE', url_video='https://www.youtube.com/embed/QHrIO139sWc')
        custom = Maquina.objects.create(nombre='Equipo propio', descripcion='Contenido del gimnasio',
                                       grupo_muscular='OT', url_video='https://youtu.be/46Ae9zoLEcg')
        call_command('cargar_guias', stdout=StringIO())
        original.refresh_from_db()
        self.assertIn('Preparación y ejecución', original.descripcion)
        self.assertEqual(original.pk, 67)
        self.assertEqual(original.youtube_id, 'QHrIO139sWc')
        self.assertEqual(obtener_guia(original)['autor'], 'Maru lekhal')
        custom.refresh_from_db()
        self.assertEqual(custom.descripcion, 'Contenido del gimnasio')
        count = Maquina.objects.count()
        call_command('cargar_guias', stdout=StringIO())
        self.assertEqual(Maquina.objects.count(), count)
        for code in ['PE', 'ES', 'PI', 'BR', 'HO', 'AB']:
            self.assertTrue(Maquina.objects.filter(grupo_muscular=code).exists())

    def test_dry_run_does_not_change_database(self):
        call_command('cargar_guias', dry_run=True, stdout=StringIO())
        self.assertEqual(Maquina.objects.count(), 0)

    def test_broken_placeholder_is_replaced_without_changing_id(self):
        machine = Maquina.objects.create(nombre='Leg Extension', descripcion='Piernas',
                                         grupo_muscular='PI',
                                         url_video='https://www.youtube.com/embed/bW8pkerbm3b1pXde')
        original_id = machine.pk
        call_command('cargar_guias', stdout=StringIO())
        machine.refresh_from_db()
        self.assertEqual(machine.pk, original_id)
        self.assertEqual(machine.youtube_id, '6itzUh4wAXc')
        response = self.client.get(reverse('detalle-maquina', args=[machine.pk]))
        for text in ['Preparación y ejecución', 'Errores que debes evitar', 'Nova Southeastern',
                     'https://www.youtube.com/watch?v=6itzUh4wAXc']:
            self.assertContains(response, text)

    def test_normalizes_real_youtube_links_and_rejects_bad_ids(self):
        for url in ['https://youtu.be/6itzUh4wAXc?t=4',
                    'https://www.youtube.com/shorts/6itzUh4wAXc',
                    'https://www.youtube.com/watch?v=6itzUh4wAXc&feature=share',
                    'https://www.youtube.com/embed/6itzUh4wAXc?rel=0']:
            self.assertEqual(Maquina(url_video=url).youtube_id, '6itzUh4wAXc')
        for url in ['https://www.youtube.com/embed/bW8pkerbm3b1pXde',
                    'https://untrusted.example/embed/6itzUh4wAXc']:
            self.assertEqual(Maquina(url_video=url).video_embed_url, '')

    def test_unrelated_video_does_not_inherit_publisher_credit(self):
        machine = Maquina(nombre='Leg Extension', url_video='https://youtu.be/46Ae9zoLEcg')
        self.assertIsNone(obtener_guia(machine))
