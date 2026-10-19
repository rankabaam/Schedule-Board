"""Generate an offline HTML view of fictional service tasks.

This is an independently written portfolio demo, not production software.
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, time
from html import escape
from pathlib import Path

REQUIRED = ('date', 'time', 'team', 'task', 'status', 'reference')
STATUSES = ('Planned', 'Confirmed', 'Changed', 'Cancelled')


def read_tasks(path):
    with Path(path).open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(REQUIRED).issubset(reader.fieldnames):
            raise ValueError('CSV must contain: ' + ', '.join(REQUIRED))
        records = []
        for line_number, record in enumerate(reader, start=2):
            row = {key: (record.get(key) or '').strip() for key in REQUIRED}
            try:
                date.fromisoformat(row['date'])
                time.fromisoformat(row['time'])
            except ValueError as exc:
                raise ValueError(f'Line {line_number}: invalid date or time') from exc
            if row['status'] not in STATUSES:
                raise ValueError(f'Line {line_number}: unknown status {row["status"]!r}')
            if not row['task'] or not row['team']:
                raise ValueError(f'Line {line_number}: team and task are required')
            records.append(row)
    return sorted(records, key=lambda r: (r['date'], r['time'], r['team']))


def build_dashboard(records):
    groups = defaultdict(list)
    for record in records:
        groups[record['date']].append(record)
    totals = Counter(r['status'] for r in records)
    summary = ''.join(
        f'<div class="tile"><span>{escape(key)}</span><b>{totals[key]}</b></div>'
        for key in STATUSES
    )
    sections = []
    for day, tasks in sorted(groups.items()):
        cards = []
        for row in tasks:
            status = row['status']
            searchable = ' '.join(row.values()).lower()
            cards.append(
                '<article class="task" data-status="' + escape(status, quote=True) +
                '" data-search="' + escape(searchable, quote=True) + '">' +
                '<div class="clock">' + escape(row['time']) + '</div>' +
                '<div><strong>' + escape(row['task']) + '</strong>' +
                '<div class="small">' + escape(row['team']) + ' · ' + escape(row['reference']) + '</div></div>' +
                '<span class="badge ' + status.lower() + '">' + escape(status) + '</span>' +
                '</article>'
            )
        sections.append('<section class="day"><h2>' + escape(day) + '</h2>' + ''.join(cards) + '</section>')
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Schedule Board · Synthetic Demo</title><style>
:root{font-family:system-ui,Arial,sans-serif;color:#19273b;background:#f4f6f8}
body{max-width:1020px;margin:30px auto;padding:0 18px}header{display:flex;justify-content:space-between;align-items:center;gap:16px}
h1{margin:0}p{color:#506173}.pill{padding:8px 12px;background:#e5edf5;border-radius:99px;font-size:12px}
.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:24px 0}.tile,.day{background:#fff;border:1px solid #dae1e9;border-radius:14px;padding:14px}
.tile span{display:block;color:#506173;font-size:13px}.tile b{font-size:27px}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:18px 0}
input[type=search]{padding:12px;border:1px solid #b7c4d1;border-radius:8px;min-width:250px;flex:1}.day{margin:16px 0}
h2{font-size:16px;margin:0 0 10px}.task{display:grid;grid-template-columns:68px 1fr auto;gap:14px;align-items:center;border-top:1px solid #e8edf2;padding:12px 0}
.clock{font-weight:700}.small{font-size:12px;color:#617086;padding-top:4px}.badge{padding:5px 9px;border-radius:6px;font-size:12px}
.confirmed{background:#dff3e9;color:#186447}.planned{background:#e6edf8;color:#275782}.changed{background:#fff0ce;color:#825000}.cancelled{background:#eee;color:#666}
[hidden]{display:none!important}footer{color:#68798e;font-size:12px;margin:28px 0}@media(max-width:600px){.summary{grid-template-columns:repeat(2,1fr)}.task{grid-template-columns:55px 1fr;gap:6px}.badge{grid-column:2;justify-self:start}}
@media print{body{margin:0}.controls{display:none}.day{break-inside:avoid}}
</style></head><body>
<header><div><h1>Schedule Board</h1><p>Fictional community-service schedule</p></div><span class="pill">SYNTHETIC DEMO</span></header>
<div class="summary">""" + summary + """</div><div class="controls"><input id="search" type="search" placeholder="Search task, team or reference" aria-label="Search tasks">
<label><input id="cancelled" type="checkbox" checked> Show cancelled</label><button onclick="window.print()">Print / Save PDF</button></div>
<main>""" + ''.join(sections) + """</main><footer>Independent portfolio demo. All records are fictional.</footer>
<script>const q=document.getElementById('search'),c=document.getElementById('cancelled');
function filter(){let s=q.value.trim().toLowerCase();document.querySelectorAll('.task').forEach(e=>e.hidden=!(e.dataset.search.includes(s)&&(c.checked||e.dataset.status!=='Cancelled')));
document.querySelectorAll('.day').forEach(d=>d.hidden=[...d.querySelectorAll('.task')].every(e=>e.hidden));}
q.addEventListener('input',filter);c.addEventListener('change',filter);</script></body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='sample_data/tasks.csv', type=Path)
    parser.add_argument('--output', default='output/schedule.html', type=Path)
    args = parser.parse_args()
    records = read_tasks(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_dashboard(records), encoding='utf-8')
    print(f'Created {args.output} from {len(records)} fictional tasks')


if __name__ == '__main__':
    main()
