from datetime import date, timedelta
import pytest
from services.timetable_service import validate_sessions

def test_invalid_time_rejected():
    d=date.today()+timedelta(days=1); exam=d+timedelta(days=2)
    s={"date":d.isoformat(),"subject":"OS","topic":"Paging","session_type":"Learning","start_time":"25:70","duration":1}
    with pytest.raises(ValueError): validate_sessions([s],exam,2)
