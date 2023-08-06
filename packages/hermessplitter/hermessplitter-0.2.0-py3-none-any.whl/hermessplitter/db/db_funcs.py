import sqlalchemy
from sqlalchemy.dialects.sqlite import insert
from hermessplitter.db import init_db
from hermessplitter.db import tables


def create_new_record(record_id: int,
                      clear_gross: int = None, hermes_gross: int = None,
                      final_gross: int = None,
                      clear_cargo: int = None , hermes_cargo: int = None,
                      final_cargo: int = None, tare: int = None,
                      test_mode: bool = None, kf_source_id: int = None,
                      notes: str = None):
    ins = tables.records.insert().values(
        record_id=record_id,
        clear_gross=clear_gross,
        hermes_gross=hermes_gross,
        final_gross=final_gross,
        clear_cargo=clear_cargo,
        hermes_cargo=hermes_cargo,
        final_cargo=final_cargo,
        tare=tare,
        test_mode=test_mode,
        kf_source_id=kf_source_id,
        notes=notes
    )
    return init_db.engine.execute(ins)


def create_or_upd_client(name: str, ex_id: str, kf: int = 0):
    ins = insert(tables.clients).values(
        name=name,
        kf=kf,
        ex_id=ex_id
    )
    on_duplicate_key = ins.on_conflict_do_update(
        index_elements=['ex_id'],
        set_=dict(kf=kf)
    )
    return init_db.engine.execute(on_duplicate_key)


def get_client_kf_by_name(name):
    ins = sqlalchemy.select(tables.clients.c.kf).where(
        tables.clients.c.name == name)
    r = init_db.engine.execute(ins)
    return r.fetchone()

def get_client_kf_by_ex_id(ex_id):
    ins = sqlalchemy.select(tables.clients.c.kf).where(
        tables.clients.c.ex_id == ex_id)
    r = init_db.engine.execute(ins)
    return r.fetchone()


def get_all_data(table):
    s = sqlalchemy.select(table)
    r = init_db.engine.execute(s)
    return r.fetchall()


def set_settings(**kwargs):
    for key, _value in kwargs.items():
        ins = insert(tables.settings).values(
            key=key,
            value=_value,
        )
        on_duplicate_key = ins.on_conflict_do_update(
            index_elements=['key'],
            set_=dict(value=_value)
        )
        return init_db.engine.execute(on_duplicate_key)


def get_hermes_activity():
    ins = sqlalchemy.select(tables.settings.c.value).where(
        tables.settings.c.key == 'active')
    r = init_db.engine.execute(ins)
    return r.fetchone()
