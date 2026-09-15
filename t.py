from app import app
import traceback
with app.test_client() as c:
    try:
        rv = c.get(" /api/attendance/summary\)
