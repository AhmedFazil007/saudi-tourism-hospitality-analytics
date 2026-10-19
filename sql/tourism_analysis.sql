-- Saudi Tourism & Hospitality Analytics (synthetic modeled data).
-- Occupancy and ADR are capacity-weighted, not official market statistics.

-- Annual visitors, accommodation revenue and capacity-weighted occupancy.
SELECT SUBSTR(month,1,4) AS year,
 SUM(estimated_visitors) AS visitors,
 ROUND(SUM(estimated_room_revenue_sar),2) AS room_revenue_sar,
 ROUND(SUM(occupancy_rate_pct*estimated_room_capacity)/NULLIF(SUM(estimated_room_capacity),0),2) AS occupancy_pct,
 ROUND(SUM(average_daily_rate_sar*estimated_room_capacity)/NULLIF(SUM(estimated_room_capacity),0),2) AS weighted_adr_sar,
 ROUND(SUM(estimated_room_revenue_sar)/NULLIF(SUM(estimated_visitors),0),2) AS revenue_per_visitor_sar
FROM tourism_monthly GROUP BY SUBSTR(month,1,4) ORDER BY year;

-- Latest-year city comparison.
SELECT city, SUM(estimated_visitors) AS visitors,
 ROUND(SUM(estimated_room_revenue_sar),2) AS room_revenue_sar,
 ROUND(SUM(occupancy_rate_pct*estimated_room_capacity)/NULLIF(SUM(estimated_room_capacity),0),2) AS occupancy_pct,
 ROUND(SUM(average_daily_rate_sar*estimated_room_capacity)/NULLIF(SUM(estimated_room_capacity),0),2) AS weighted_adr_sar
FROM tourism_monthly
WHERE SUBSTR(month,1,4)=(SELECT MAX(SUBSTR(month,1,4)) FROM tourism_monthly)
GROUP BY city ORDER BY room_revenue_sar DESC;

-- Monthly visitor and revenue patterns.
SELECT month, SUM(estimated_visitors) AS visitors,
 ROUND(SUM(estimated_room_revenue_sar),2) AS room_revenue_sar
FROM tourism_monthly GROUP BY month ORDER BY month;

-- Accommodation types in latest year: sampled/modelled observations only.
SELECT accommodation_type, COUNT(*) AS observations,
 SUM(estimated_visitors) AS visitors,
 ROUND(SUM(estimated_room_revenue_sar),2) AS room_revenue_sar,
 ROUND(SUM(occupancy_rate_pct*estimated_room_capacity)/NULLIF(SUM(estimated_room_capacity),0),2) AS occupancy_pct
FROM tourism_monthly
WHERE SUBSTR(month,1,4)=(SELECT MAX(SUBSTR(month,1,4)) FROM tourism_monthly)
GROUP BY accommodation_type ORDER BY room_revenue_sar DESC;
