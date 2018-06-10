from django.core.management.base import BaseCommand

from hub.apps.content.types.academic import AcademicProgram

class Command(BaseCommand):
    help = 'Update imported academic programs to the correct permission'

    def handle(self, *args, **options):

        acad_prog = AcademicProgram.objects.filter(permission='member')

        for program in acad_prog:
            program.permission = 'open'
            program.save()

        return
