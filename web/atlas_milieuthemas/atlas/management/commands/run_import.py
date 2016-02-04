from django.core.management import BaseCommand

from datapunt_generic.batch import batch

import datasets.themas.batch
import datasets.schiphol.batch


class Command(BaseCommand):
    ordered = [
        'themas',
        'schiphol'
    ]

    imports = dict(
        themas=[
            datasets.themas.batch.ImportThemasJob,
        ],
        schiphol=[
            datasets.schiphol.batch.ImportSchipholJob,
        ],
    )

    def add_arguments(self, parser):
        parser.add_argument('dataset',
                            nargs='*',
                            default=self.ordered,
                            help="Dataset to import, choose from {}".format(', '.join(self.imports.keys())))

        parser.add_argument('--no-import',
                            action='store_false',
                            dest='run-import',
                            default=True,
                            help='Skip database importing')

    def handle(self, *args, **options):
        dataset = options['dataset']

        for ds in dataset:
            if ds not in self.imports.keys():
                self.stderr.write("Unkown dataset: {}".format(ds))
                return

        sets = [ds for ds in self.ordered if ds in dataset]     # enforce order

        self.stdout.write("Importing {}".format(", ".join(sets)))

        for ds in sets:
            if options['run-import']:
                for job_class in self.imports[ds]:
                    batch.execute(job_class())