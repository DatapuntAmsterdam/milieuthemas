"""
Batch importing task for the Risicozones infrastructuur
"""

# Python
import logging
import os
# Packages
from django.contrib.gis.geos import GeometryCollection, GEOSGeometry, LineString, MultiLineString, MultiPolygon, Polygon
from django.contrib.gis.geos.error import GEOSException
# Project
from .models import Infrastructuur
from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from datapunt_generic.generic.csv import process_csv


log = logging.getLogger(__name__)  # pylint: disable=C0103


class ImportInfrastructuurBase(batch.BasicTask):
    """
    Base class for the infrastructuur imports
    Most code is implemented here. Subclasses just need to set the parameters.

    Required subclass parameters:
    name - the task name
    type - The type of infrastructure
    source_file - the CSV source file

    The subclass must implement the following functions:
    prepare_geos - Prepares the geos data for the model.
    """

    def before(self):
        """
        Cleaning all the data beofre a new import
        """
        database.clear_model_by_value(Infrastructuur, 'type', self.type)

    def after(self):
        pass

    def process(self):
        """
        Process the csv file, bulk creating the data from it
        """
        source = os.path.join(self.path, self.source_file)
        # Processing csv
        entries = [entry for entry in process_csv(source, self.process_row) if entry]
        # Bulk creating valid entries
        Infrastructuur.objects.bulk_create(entries, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        Handle CSV row
        """
        # geometrie is the only actual data. If not present there is no point
        # in importing
        if not row['geometrie']:
            return None
        try:
            geom = GEOSGeometry(row['geometrie'])
            geom = self.prepare_geos(geom)
        except GEOSException as msg:
            log.warn('%s id %d unable to encapsulate GEOS geometry %s; skipping', self.model, row['id'], msg)
            return None
        return Infrastructuur(type=self.type, geometrie_line=geom['line'], geometrie_polygon=geom['poly'])


class ImportAardgasbuisleidingTask(ImportInfrastructuurBase):
    """
    Aardgas buis leiding import task
    """
    name = 'Import dmb_aardgas_leiding'
    type = 'ag'
    source_file = 'dmb_aardgas_leiding.csv'

    def prepare_geos(self, geom):
        # Converting to a MultiLineString
        if isinstance(geom, LineString):
            geom = MultiLineString([geom])
        elif not isinstance(geom, MultiLineString) and isinstance(geom, GeometryCollection):
            # Converting to MultiLineString
            lines = []
            for item in geom:
                if isinstance(item, LineString):
                    lines.append(item)
                elif isinstance(item, Polygon):
                    for poly_item in item:
                        # Line ring are managable
                        if poly_item.geom_type == 'LinearRing':
                            lines.append(LineString(poly_item.coords))
                        else:
                            raise GEOSException('Polygon in GeometryCollection with unmanagable components')
                else:
                    raise GEOSException('GeometryCollection with unmanagable components')
            geom = MultiLineString(lines)
        return {'line': geom, 'poly': None}


class ImportSpoorwegTask(ImportInfrastructuurBase):
    """
    Spoorweg import task
    """
    name = 'Import dro_risico_spoorweg'
    type = 'sw'
    source_file = 'dro_risico_spoorweg.csv'

    def prepare_geos(self, geom):
        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)
        elif not isinstance(geom, MultiPolygon):
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)
        return {'line': None, 'poly': geom}


class ImportVaarwegTask(ImportInfrastructuurBase):
    """
    Spoorweg import task
    """
    name = 'Import dro_risico_vaarweg'
    type = 'vw'
    source_file = 'dro_risico_vaarweg.csv'

    def prepare_geos(self, geom):
        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)
        elif not isinstance(geom, MultiPolygon):
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)
        return {'line': None, 'poly': geom}


class ImportWegTask(ImportInfrastructuurBase):
    """
    Spoorweg import task
    """
    name = 'Import dro_risico_weg'
    type = 'wg'
    source_file = 'dro_risico_weg.csv'

    def prepare_geos(self, geom):
        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)
        elif not isinstance(geom, MultiPolygon):
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)
        return {'line': None, 'poly': geom}


class ImportRisicozonesInfrastructuurJob(object):
    """
    Import tasks listing for the risicozones infrasctuctuur dataset
    """
    name = 'Import risicozones infrastructuur'

    def tasks(self):
        """
        Return the list of tasks to run
        """
        return [
            ImportAardgasbuisleidingTask(),
            ImportSpoorwegTask(),
            ImportVaarwegTask(),
            ImportWegTask(),
        ]
