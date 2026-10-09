# PhD timeline Gantt chart (vector PDF for my prospectus presentation).
This python script makes a Gantt Chart timeline describing 4 phases of my PhD. Each Phase has several tasks below it. All tasks are labeled either "Completed" (green), "In progress" (Yellow), "Planned" (Grey). Each phase ends with a milestone paper or graduation date. Each milestone is labeled by a blue diamond and the paper title is listed below it.

Structure:
  * one dark summary bar spanning each whole phase
  * individual task bars beneath, colored by status
  * publication / graduation as blue diamond milestones, each labeled
    directly with its paper title via a short leader line (no separate key)
  * year + quarter header, quarter gridlines

TO EDIT
  - All content lives in the PHASES list below. Each task is
    (label, status, start_date, end_date, estimated_flag).
  - status is one of: "done", "prog", "plan".
  - Dates are datetime.date(YYYY, M, D). For a bar to cover a whole
    month, end it on the FIRST of the following month.
  - estimated_flag=True just tags guesses in the console printout.
  - Milestones are (ms_number, full_name, date). The full_name is drawn
    beside the diamond with a leader line; ms_number is unused for display
    now (kept so you can switch back to short tags if you want).
  - Colors live in COLORS at the top.
