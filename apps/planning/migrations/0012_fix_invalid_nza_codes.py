from django.db import migrations

def fix_invalid_nza_codes(apps, schema_editor):
    Werkbon = apps.get_model('planning', 'Werkbon')
    for wb in Werkbon.objects.all():
        # Probeer de waarde van het nza_code_id attribuut op te halen, gebruik None als fallback
        value = getattr(wb, 'nza_code_id', None)
        if value is not None:
            try:
                # Probeer de waarde naar een integer om te zetten
                int(value)
            except (ValueError, TypeError):
                wb.nza_code = None
                wb.save()
        # Als het attribuut helemaal niet bestaat, reset dan het nza_code veld
        else:
            wb.nza_code = None
            wb.save()

class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0011_fix_invalid_nza_codes'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_nza_codes),
    ]
