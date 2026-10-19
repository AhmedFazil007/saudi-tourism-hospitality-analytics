"""Reproduce summary tables for a synthetic Saudi tourism dataset using Python's standard library."""
from pathlib import Path
from collections import defaultdict
import csv, json, sqlite3

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/01_tourism_monthly_synthetic.csv"
OUT=ROOT/"analysis"
OUT.mkdir(exist_ok=True)
FIELDS=["month","city","region","accommodation_type","estimated_room_capacity","occupancy_rate_pct","average_daily_rate_sar","average_length_of_stay_nights","estimated_visitors","estimated_room_revenue_sar"]
with DATA.open(encoding="utf-8-sig",newline="") as f:
 reader=csv.DictReader(f)
 assert reader.fieldnames==FIELDS,"Unexpected columns"
 rows=list(reader)
assert rows,"Empty dataset"
for r in rows:
 for k in ("estimated_room_capacity","estimated_visitors"):r[k]=int(r[k])
 for k in ("occupancy_rate_pct","average_daily_rate_sar","average_length_of_stay_nights","estimated_room_revenue_sar"):r[k]=float(r[k])
 assert 0<=r["occupancy_rate_pct"]<=100
 assert r["estimated_room_capacity"]>=0 and r["estimated_visitors"]>=0 and r["estimated_room_revenue_sar"]>=0
 r["year"]=r["month"][:4]
assert len({(r["month"],r["city"]) for r in rows})==len(rows),"Duplicate city-month"
def summarize(data):
 cap=sum(r["estimated_room_capacity"] for r in data)
 visitors=sum(r["estimated_visitors"] for r in data)
 revenue=sum(r["estimated_room_revenue_sar"] for r in data)
 return {"estimated_visitors":visitors,"estimated_room_revenue_sar":round(revenue,2),
 "capacity_weighted_occupancy_pct":round(sum(r["occupancy_rate_pct"]*r["estimated_room_capacity"] for r in data)/cap,2) if cap else None,
 "capacity_weighted_adr_sar":round(sum(r["average_daily_rate_sar"]*r["estimated_room_capacity"] for r in data)/cap,2) if cap else None,
 "revenue_per_estimated_visitor_sar":round(revenue/visitors,2) if visitors else None}
def export(filename,keys,data):
 groups=defaultdict(list)
 for r in data:groups[tuple(r[k] for k in keys)].append(r)
 records=[dict(zip(keys,key),**summarize(group)) for key,group in sorted(groups.items())]
 with (OUT/filename).open("w",newline="",encoding="utf-8") as f:
  writer=csv.DictWriter(f,fieldnames=keys+list(summarize(rows)))
  writer.writeheader();writer.writerows(records)
 return records
monthly=export("monthly_summary.csv",["month"],rows)
yearly=export("yearly_summary.csv",["year"],rows)
city=export("city_summary.csv",["city"],rows)
export("city_year_summary.csv",["year","city"],rows)
export("accommodation_summary.csv",["accommodation_type"],rows)
export("accommodation_year_summary.csv",["year","accommodation_type"],rows)
latest=max(r["year"] for r in rows)
recent=[r for r in rows if r["year"]==latest]
export("latest_year_city.csv",["city"],recent)
export("latest_year_accommodation.csv",["accommodation_type"],recent)
con=sqlite3.connect(OUT/"tourism.sqlite")
try:
 con.execute("DROP TABLE IF EXISTS tourism_monthly")
 con.execute("""CREATE TABLE tourism_monthly(month TEXT NOT NULL,city TEXT NOT NULL,region TEXT NOT NULL,accommodation_type TEXT NOT NULL,estimated_room_capacity INTEGER,occupancy_rate_pct REAL,average_daily_rate_sar REAL,average_length_of_stay_nights REAL,estimated_visitors INTEGER,estimated_room_revenue_sar REAL,PRIMARY KEY(month,city))""")
 con.executemany("INSERT INTO tourism_monthly VALUES (?,?,?,?,?,?,?,?,?,?)",[tuple(r[c] for c in FIELDS) for r in rows])
 con.commit()
finally:con.close()
summary={"dataset":"Synthetic modeled tourism observations, not official Saudi tourism statistics","records":len(rows),"months":len(monthly),"cities":len(city),"latest_year":latest,"overall":summarize(rows),"latest_year_summary":summarize(recent),"first_year_summary":summarize([r for r in rows if r["year"]==min(x["year"] for x in rows)])}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
