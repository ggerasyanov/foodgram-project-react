import csv

from recipes.models import Ingredient

csv_file_path = ('./data/ingredients.csv')

with open(csv_file_path, encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        created = Ingredient.objects.get_or_create(
            name=row['name'],
            measurement_unit=row['measurement_unit']
        )