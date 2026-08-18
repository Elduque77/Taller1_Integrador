import csv
import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Carga las películas iniciales desde un archivo CSV a la base de datos'

    def handle(self, *args, **kwargs):
        # Ruta al archivo CSV
        csv_path = os.path.join(os.path.dirname(__file__), 'movies_initial.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo: {csv_path}'))
            return

        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                # Verifica si la película ya existe para evitar duplicados
                if not Movie.objects.filter(title=row['title']).exists():
                    Movie.objects.create(
                        title=row['title'],
                        description=row.get('description', ''),
                        image=row.get('image', ''),
                        url=row.get('url', '')
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Se agregaron {count} películas exitosamente a la base de datos.'))