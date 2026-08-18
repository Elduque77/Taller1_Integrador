import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Carga las películas iniciales desde un archivo CSV a la base de datos'

    def handle(self, *args, **kwargs):
        # Elimina los registros anteriores para evitar duplicados en inglés
        Movie.objects.all().delete()

        # Busca el CSV tanto en la raíz como en la carpeta del comando
        csv_path = os.path.join(settings.BASE_DIR, 'movies_initial.csv')
        if not os.path.exists(csv_path):
            csv_path = os.path.join(os.path.dirname(__file__), 'movies_initial.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo: {csv_path}'))
            return

        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                Movie.objects.create(
                    title=row['title'],
                    description=row.get('description', ''),
                    image=row.get('image', ''),
                    url=row.get('url', ''),
                    genre=row.get('genre', 'General'),
                    year=int(row['year']) if row.get('year') else None
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Se agregaron {count} películas exitosamente.'))