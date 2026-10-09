#!/usr/bin/env python3

from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D

# --------------------------------------------------------------------------
COLORS = {
    "phase": "#2b2b2b",   # phase summary bar (near-black)
    "done":  "#4c7a34",   # completed      (green)
    "prog":  "#e0a526",   # in progress    (amber)
    "plan":  "#9aa6b2",   # planned        (grey-blue)
    "mile":  "#2f6db5",   # milestone      (blue)
    "grid":  "#c9c9c9",
    "yeargrid": "#8a8a8a",
    "header": "#f0f0f0",
}
TASK_H, PHASE_H = 0.52, 0.60
MS_DROP = 1          # how far the milestone drop-line falls below the phase bar (rows)

# --------------------------------------------------------------------------
# CONTENT  --  edit here.  tasks: (label, status, start, end, estimated?)
# --------------------------------------------------------------------------
PHASES = [
    {
        "name": "Phase 1 \u2014 Single-particle loading",
        "start": date(2024, 9, 1), "end": date(2027, 5, 15),
        "tasks": [
            ("Build prototype Paul trap",              "done", date(2024, 9, 1),  date(2025, 3, 1),  False),
            ("Single-drop loading (prototype)", "done", date(2025, 2, 1),  date(2025, 11, 30), False),
            ("Vacuum Paul trap commissioning",  "done", date(2025, 12, 1),  date(2026, 6, 1),  False),
            ("Recover single-drop loading",      "prog", date(2026, 6, 1),  date(2026, 10, 1), False),
            #("Nanoparticle loading-efficiency trials", "plan", date(2026, 10, 1), date(2027, 2, 15), False),
            ("Load undoped sphere into optical trap",  "plan", date(2026, 10, 1), date(2027, 5, 1),  False),
        ],
        "milestones": [("MS1", "Single-Particle Loading Paper", date(2027, 5, 15))],
    },
    {
        "name": "Phase 2 \u2014 $^{18}$F loading & coincidence",
        "start": date(2026, 5, 1), "end": date(2027, 9, 30),
        "tasks": [
            ("Impulse Time Resolution",         "prog", date(2026, 5, 1),  date(2026, 10, 1), False),
            (r"Optimize $^{18}$F trapping",            "prog", date(2026, 6, 1),  date(2027, 5, 1),  False),
            # ("Time res.: impulse calibration",         "prog", date(2026, 5, 1),  date(2026, 10, 1), False),
            ("Double-Coincidence Signals",          "plan", date(2026, 10, 1), date(2027, 4, 1),  True),
            (r"$\nu$ momentum from $^{18}$F recoils",  "plan", date(2027, 3, 1),  date(2027, 9, 30),  True),
        ],
        "milestones": [("MS2", r"$^{18}$F $\nu$ momentum paper", date(2027, 9, 30))],
    },
    {
        "name": "Phase 3 \u2014 Sterile search ($^{90}$Y / $^{51}$Cr)",
        "start": date(2027, 8, 15), "end": date(2029, 1, 1),
        "tasks": [
            #("Doping trials per isotope",              "plan", date(2027, 10, 1), date(2028, 1, 1),  False),
            ("Background characterization",         "plan", date(2027, 8, 15),date(2028, 1, 15),  False),
            ("Radioactive loading",  "plan", date(2028, 1, 1),  date(2028, 6, 1),  False),
            #("3D homodyne upgrade & CMOS deployment",      "plan", date(2028, 2, 15), date(2028, 7, 1),  False),
            (r"Sterile $\nu$ search",  "plan", date(2028, 4, 1),  date(2028, 7, 1),  False),
            ("Data analysis & paper writing",          "plan", date(2028, 7, 1),  date(2029, 1, 1),  False),
        ],
        "milestones": [("MS3", r"Sterile $\nu$ Search paper", date(2029, 1, 1))],
    },
    {
        "name": "Phase 4 \u2014 Thesis",
        "start": date(2029, 1, 1), "end": date(2029, 8, 22),
        "tasks": [
            ("Thesis writing", "plan", date(2029, 1, 1), date(2029, 7, 1), False),
        ],
        "milestones": [("MS4", "Graduation", date(2029, 8, 22))],
    },
]

X_MIN, X_MAX = date(2024, 8, 1), date(2030, 1, 1)   # right edge extended to fit drawn-out labels

# --------------------------------------------------------------------------
rows = []
for ph in PHASES:
    rows.append({"kind": "phase", "label": ph["name"],
                 "start": ph["start"], "end": ph["end"],
                 "milestones": ph.get("milestones", [])})
    for (label, status, s, e, est) in ph["tasks"]:
        rows.append({"kind": "task", "label": label, "status": status,
                     "start": s, "end": e, "est": est})

R = len(rows)
def y_of(i): return R - 1 - i

fig, ax = plt.subplots(figsize=(15, 8.5))
xmin_n, xmax_n = mdates.date2num(X_MIN), mdates.date2num(X_MAX)

def months(d0, d1, step):
    y, m, out = d0.year, d0.month, []
    while date(y, m, 1) <= d1:
        out.append(date(y, m, 1)); m += step
        while m > 12: m -= 12; y += 1
    return out

grid_top = R - 0.4
for q in months(date(2024, 1, 1), X_MAX, 3):
    xn = mdates.date2num(q)
    if xmin_n <= xn <= xmax_n:
        yr = (q.month == 1)
        ax.plot([xn, xn], [-0.5, grid_top],
                color=COLORS["yeargrid"] if yr else COLORS["grid"],
                lw=1.0 if yr else 0.6, ls="-" if yr else (0, (1, 2)), zorder=0)

# ---- bars + milestones (drawn out with leader lines) ----
for i, row in enumerate(rows):
    y = y_of(i)
    s_n, e_n = mdates.date2num(row["start"]), mdates.date2num(row["end"])
    if row["kind"] == "phase":
        ax.barh(y, e_n - s_n, left=s_n, height=PHASE_H, color=COLORS["phase"], zorder=3)
        for (ms, name, d) in row["milestones"]:
            mn = mdates.date2num(d)
            # vertical drop-line from the diamond, then the paper title beside its foot
            ax.plot([mn, mn], [y, y - MS_DROP], color=COLORS["mile"], lw=1.0, zorder=5)
            ax.plot(mn, y, marker="D", ms=11, color=COLORS["mile"],
                    markeredgecolor="white", markeredgewidth=1.0, zorder=6)
            ax.annotate(name, (mn, y - MS_DROP), xytext=(5, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=10,
                        color=COLORS["mile"], zorder=7)
    else:
        ax.barh(y, e_n - s_n, left=s_n, height=TASK_H, color=COLORS[row["status"]],
                edgecolor="white", linewidth=0.6, zorder=3)

# ---- y labels ----
ax.set_yticks([y_of(i) for i in range(R)])
ax.set_yticklabels([r["label"] if r["kind"] == "phase" else "    " + r["label"] for r in rows],
                   fontsize=9.5)
for tick, row in zip(ax.get_yticklabels(), rows):
    if row["kind"] == "phase":
        tick.set_fontweight("bold"); tick.set_fontsize(10.5)
    else:
        tick.set_color("#333333")

# ---- header bands ----
q_band, y_band = (R - 0.35, R + 0.55), (R + 0.55, R + 1.55)
def add_band(y0, y1, cells, fontsize, weight):
    for (c0, c1, text) in cells:
        x0, x1 = max(mdates.date2num(c0), xmin_n), min(mdates.date2num(c1), xmax_n)
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=COLORS["header"],
                               edgecolor=COLORS["yeargrid"], lw=0.8, zorder=2))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, text, ha="center", va="center",
                fontsize=fontsize, fontweight=weight, zorder=4)

qcells = []
for q in months(date(2024, 1, 1), X_MAX, 3):
    nm, ny = q.month + 3, q.year
    while nm > 12: nm -= 12; ny += 1
    q_next = date(ny, nm, 1)
    if mdates.date2num(q_next) <= xmin_n or mdates.date2num(q) >= xmax_n: continue
    qcells.append((q, q_next, f"Q{(q.month - 1)//3 + 1}"))
add_band(*q_band, qcells, 8.5, "normal")

ycells = []
for yr in range(2024, 2030):
    ys, ye = date(yr, 1, 1), date(yr + 1, 1, 1)
    if mdates.date2num(ye) <= xmin_n or mdates.date2num(ys) >= xmax_n: continue
    ycells.append((ys, ye, str(yr)))
add_band(*y_band, ycells, 11, "bold")

# ---- cosmetics ----
ax.set_xlim(xmin_n, xmax_n)
ax.set_ylim(-0.6, R + 1.7)
ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)

legend_items = [
    Patch(facecolor=COLORS["phase"], label="Phase"),
    Patch(facecolor=COLORS["done"],  label="Completed"),
    Patch(facecolor=COLORS["prog"],  label="In progress"),
    Patch(facecolor=COLORS["plan"],  label="Planned"),
    Line2D([0], [0], marker="D", color="w", markerfacecolor=COLORS["mile"],
           markersize=10, label="Milestone"),
]
ax.legend(handles=legend_items, loc="lower left", bbox_to_anchor=(0.0, -0.09),
          ncol=5, frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("/Users/jacquelinebaeza-rubio/Downloads/SIMPLE/Prospectus/figures/timeline/timeline_gantt.pdf", bbox_inches="tight")
plt.savefig("/Users/jacquelinebaeza-rubio/Downloads/SIMPLE/Prospectus/figures/timeline/timeline_gantt_preview.png", dpi=130, bbox_inches="tight")

print("Estimated (guessed) durations still to confirm:")
for ph in PHASES:
    for (label, status, s, e, est) in ph["tasks"]:
        if est:
            print(f"  [{ph['name'].split(chr(8212))[0].strip()}] {label}: {s} -> {e}")
print("\nSaved timeline_gantt.pdf and timeline_gantt_preview.png")
