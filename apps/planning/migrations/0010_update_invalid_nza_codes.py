from django.db import migrations

def fix_invalid_nza_codes(apps, schema_editor):
    Werkbon = apps.get_model('planning', 'Werkbon')
    for wb in Werkbon.objects.all():
        try:
            # Probeer de huidige waarde om te zetten naar int
            int(wb.nza_code_id)
        except (ValueError, TypeError):
            wb.nza_code = None
            wb.save()

class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0009_alter_werkbon_nza_code'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_nza_codes),
    ]
