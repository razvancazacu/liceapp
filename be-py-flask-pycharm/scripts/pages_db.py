from scripts import orar_ocr
import sqlalchemy as db
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker


def insert_page_title(session, orare, page):
    insert_stmt = insert(orare).values(nume_orar=page.titlu)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(nume_orar=insert_stmt.inserted.nume_orar)
    session.execute(on_duplicate_key_stmt)
    return session.execute(db.select([orare]).where(orare.columns.nume_orar == page.titlu)).fetchone()[0]


def insert_warning(session, warnings, warning_data, page_id):
    insert_stmt = insert(warnings).values(warning_details=warning_data, id_orar=page_id)
    session.execute(insert_stmt)


def insert_hour(o, ore, page_id, session):
    insert_stmt = insert(ore).values(
        id_orar=page_id,
        ora_inceput=o.ora_inceput,
        ora_final=o.ora_final,
        profesor=o.profesor,
        materie=o.materie,
        sala=o.sala,
        saptamana=o.saptamana,
        grupa=o.grupa
    )
    session.execute(insert_stmt)


def delete_old_table_data(session, schedules, hours, warnings):
    session.execute(db.delete(hours))
    session.execute(db.delete(warnings))
    session.execute(db.delete(schedules))


def mysql_connection(pages):
    engine = db.create_engine('mysql://root:rootalchemy@localhost/alchemydb')
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        metadata = db.MetaData()

        schedules = db.Table('orare', metadata, autoload=True, autoload_with=engine)
        hours = db.Table('ore', metadata, autoload=True, autoload_with=engine)
        warnings = db.Table('warnings', metadata, autoload=True, autoload_with=engine)

        delete_old_table_data(session, schedules, hours, warnings)

        for page in pages:
            page_id = insert_page_title(session, schedules, page)

            for warn in page.warnings:
                insert_warning(session, warnings, warn, page_id)

            for o in page.ore:
                insert_hour(o, hours, page_id, session)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    mysql_connection(orar_ocr.get_pages())
