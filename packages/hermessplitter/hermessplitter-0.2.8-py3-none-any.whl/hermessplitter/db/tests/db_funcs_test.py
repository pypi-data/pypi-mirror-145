import unittest
import sqlalchemy
from hermessplitter.db import init_db
from hermessplitter.db import db_funcs
from hermessplitter.db import tables


class TestCase(unittest.TestCase):
    def test_insert_record(self):
        record_id = 1
        result = db_funcs.create_new_record(record_id=record_id,
                                            clear_gross=5000,
                                            hermes_gross=2000,
                                            final_gross=7000,
                                            clear_cargo=3000,
                                            hermes_cargo=2000,
                                            final_cargo=5000,
                                            tare=2000,
                                            )
        self.assertTrue(isinstance(result.inserted_primary_key[0], int))
        tables.records.delete(tables.records.c.record_id == record_id)

    def test_insert_client(self):
        client_name = 'САХ, ООО'
        kf = 20
        ex_id = 123
        result = db_funcs.create_or_upd_client(name=client_name,
                                               ex_id=ex_id,
                                               kf=kf,)
        self.assertTrue(isinstance(result.inserted_primary_key[0], int))
        new_kf = 50
        result = db_funcs.create_or_upd_client(name=client_name,
                                               kf=new_kf,
                                               ex_id=ex_id)
        kf_r = db_funcs.get_client_kf_by_name(client_name)
        print('CLIENTS:', db_funcs.get_all_data(tables.clients))
        self.assertEqual(kf_r[0], new_kf)
        r = sqlalchemy.delete(tables.clients).where(tables.clients.c.name.like(client_name))
        init_db.engine.execute(r)

    def test_settings(self):
        db_funcs.set_settings(active=False)
        ins = tables.settings.select()
        r = init_db.engine.execute(ins)
        activity = db_funcs.get_hermes_activity()
        self.assertEqual(activity[0], '0')


if __name__ == '__main__':
    unittest.main()
