import time
from sqlalchemy.orm import sessionmaker
from schema import db_connect, create_nvd_tables
from schema import CveItem, CpeItem


class DataPipeline(object):
    """pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_nvd_tables(engine)
        self._Session = sessionmaker(bind=engine)

    def process_cve(self, cve_entry):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self._Session()

        cve_item = CveItem(**cve_entry)

        try:
            session.add(cve_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return

    def process_cve_many(self, cve_entries):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self._Session()
        for cve_entry in cve_entries:
            cve_item = CveItem(**cve_entry)
            session.add(cve_item)
        print('[+] Bulk processing started')

        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return

    def query_cpe(self, cpe_entry):
        session = self._Session()
        query_result = session.query(CveItem).filter(CveItem.software_list.any(cpe_entry)).all()
        return query_result

    def query_cve(self, cve_entry):
        session = self._Session()
        query_result = session.query(CveItem).filter(CveItem.cve_id == cve_entry).all()
        return query_result

    def query_year(self, cve_year):
        session = self._Session()
        query_result = session.query(CveItem).filter(CveItem.cve_id.like(cve_year))
        return  query_result

    def process_cpe(self, cpe_entry):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """

        session = self._Session()


        cpe_item = CpeItem(**cpe_entry)

        try:
            session.add(cpe_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return

    def process_cpe_many(self, cpe_entries):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """

        session = self._Session()

        for cpe_entry in cpe_entries:
            cpe_item = CpeItem(**cpe_entry)
            session.add(cpe_item)
        print("[+] Bulk Insert initated")
        try:

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return

def test_cpe_insert():
    pipeline = DataPipeline()

    cpe_entry = dict()
    cpe_entry['cpe_id'] = 'CPE:/a'
    cpe_entry['cves'] = ['1', '2', 'apple']
    # cpe_entry['title'] = 'test'
    # cpe_entry['product_catalog'] = 'test'
    # cpe_entry['vendor_website'] = 'http://'
    # cpe_entry['modification_date'] = time.strftime("%m-%d-%Y")
    # cpe_entry['status'] = "Done"
    # cpe_entry['nvd_id'] = 1111

    pipeline.process_cpe(cpe_entry)

def test_cve_insert():
    pipeline = DataPipeline()

    cve_item = dict()

    cve_item['cve_id'] = 'CVE-1234-1124'
    cve_item['configuration_id'] = "Config"
    cve_item['software_list'] = ['abcd', 'efgh']
    cve_item['publish_date'] = time.strftime("%m-%d-%Y")
    cve_item['modified_date'] = time.strftime("%m-%d-%Y")
    cve_item['Base_Score'] = 4.3
    cve_item['Base_Access_Vector'] = "None"
    cve_item['Base_Access_Complexity'] = "None"
    cve_item['Base_Authentication'] = "None"
    cve_item['Base_Confidentiality_Impact'] = "None"
    cve_item['Base_Integrity_Impact'] = "None"
    cve_item['Base_Availability_Impact'] = "None"
    cve_item['Base_Source'] = "None"
    cve_item['Base_generation'] = time.strftime("%m-%d-%Y")
    cve_item['cwe_id']  = ['123', 'abc']
    cve_item['vulnerability_source'] = ['123', 'abc']
    cve_item['vulnerability_source_reference'] = ['123', '123ab']
    cve_item['summary'] = "s 3 14234 BACDEFSDFD r234n aple"

    pipeline.process_cve(cve_item)

if __name__ == '__main__':

    # pipeline.process_cve(cpe_item)
    # pipeline.process_cpe(cpe_item)
    print("Import DataPipeline for data processing")
    test_cpe_insert()
    test_cve_insert()
