import os
import tempfile
import pytest

def test_database_crud(monkeypatch):
    import config
    fd,path=tempfile.mkstemp(suffix=".db"); os.close(fd)
    monkeypatch.setattr(config,"DB_PATH",path)
    import database.db as db
    monkeypatch.setattr(db,"DB_PATH",path)
    db.init_db()
    sid=db.add_subject("Databases","Hard")
    db.add_topic(sid,"Normalization")
    assert db.list_subjects()[0]["name"]=="Databases"
    assert db.list_topics(sid)[0]["name"]=="Normalization"
    db.set_topic_complete(db.list_topics(sid)[0]["id"],True)
    assert db.list_topics(sid)[0]["completed"]==1
    db.delete_subject(sid)
    assert db.list_subjects()==[]
    os.remove(path)
