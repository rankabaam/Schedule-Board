import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from schedule_board import build_dashboard, read_tasks


class ScheduleTests(unittest.TestCase):
    def test_demo_data_loads_and_sorts(self):
        rows = read_tasks(Path(__file__).resolve().parents[1] / 'sample_data/tasks.csv')
        self.assertEqual(7, len(rows))
        self.assertEqual(sorted((r['date'], r['time']) for r in rows), [(r['date'], r['time']) for r in rows])

    def test_markup_is_escaped(self):
        row = {'date': '2026-10-18', 'time': '08:00', 'team': 'Example', 'task': '<script>alert(1)</script>', 'status': 'Planned', 'reference': 'T-1'}
        page = build_dashboard([row])
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>alert(1)</script>', page)

    def test_bad_status_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'bad.csv'
            p.write_text('date,time,team,task,status,reference\n2026-10-18,10:00,X,Y,Unknown,Z\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unknown status'):
                read_tasks(p)


if __name__ == '__main__':
    unittest.main()
