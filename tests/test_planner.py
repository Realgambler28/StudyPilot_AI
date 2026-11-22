from datetime import date, timedelta
import pytest
from services.timetable_service import days_remaining, validate_sessions, rule_based_plan

def test_days_remaining():
    today=date(2026,1,1)
    assert days_remaining(date(2026,1,8),today)==7

def test_validate_accepts_valid_session():
    tomorrow=date.today()+timedelta(days=1)
    exam=tomorrow+timedelta(days=2)
    s=[{"date":tomorrow.isoformat(),"subject":"Math","topic":"Matrices","session_type":"Learning","start_time":"09:00","duration":2}]
    assert validate_sessions(s,exam,3)

def test_rejects_after_exam():
    exam=date.today()+timedelta(days=1)
    s=[{"date":exam.isoformat(),"subject":"Math","topic":"Matrices","session_type":"Learning","start_time":"09:00","duration":1}]
    with pytest.raises(ValueError): validate_sessions(s,exam,3)

def test_rejects_daily_limit():
    d=date.today()+timedelta(days=1); exam=d+timedelta(days=1)
    base={"date":d.isoformat(),"subject":"Math","topic":"A","session_type":"Learning","start_time":"09:00","duration":2}
    with pytest.raises(ValueError): validate_sessions([base,dict(base,topic="B",start_time="11:00")],exam,3)

def test_rule_plan_uses_only_given_topics():
    start=date.today(); exam=start+timedelta(days=10)
    plan=rule_based_plan([{"name":"DBMS","difficulty":"Hard","topics":[{"name":"Normalization"}]}],exam,2,start)
    assert plan and all(x["topic"]=="Normalization" for x in plan)
