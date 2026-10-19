# Opening the Power BI project

1. Open `powerbi/Saudi_Tourism.pbip` in a recent version of Power BI Desktop.
2. Select **Transform data → Edit parameters** and change `CSVFilePath` to the absolute path of `data/01_tourism_monthly_synthetic.csv` on your machine.
3. Choose **Close & Apply**, then **Refresh**.
4. Check the four pages: Tourism Demand & Visitor Trends; City Tourism Performance; Accommodation Revenue & Pricing; Accommodation & Guest Mix.
5. Save a standalone `.pbix` in Power BI Desktop if desired.

## Display conventions

- Revenue and average daily rate (ADR): Saudi riyals (**SAR**).
- Occupancy: **percentages**. Source percentages are divided by 100 in the DAX measure.
- Visitors: whole numbers, with **K/M** units on large visuals where appropriate.
- Layout: 1200 × 675 report canvas with consistent titles, KPI cards and slicers.

The PBIP was generated from an editable report template and checked structurally. It has **not been opened or visually validated in Power BI Desktop** here; verify the refreshed report, formatting and slicer behavior before publishing.
