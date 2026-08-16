"""ASCII / HTML / PDF contract table. Sort is vs-ask."""

from __future__ import annotations

from pathlib import Path

from options_offshoot.config import EXPORT_DIR, MODEL_VERSION
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.localtime import filename_stamp, now_eastern_text
from options_offshoot.models.schemas import FieldRun, RankedContract


def _fmt_edge(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.3f}"


def _fmt_p(row: RankedContract) -> str:
    p = row.model.p_itm
    if p is None:
        return "n/a"
    lo = row.model.p_itm_low
    hi = row.model.p_itm_high
    if lo is None or hi is None:
        return f"{p:.3f}"
    return f"{p:.3f} [{lo:.2f}-{hi:.2f}]"


def format_table(run: FieldRun) -> str:
    lines = [
        f"OPTIONS FIELD  {run.field_id}  {MODEL_VERSION}",
        f"printed {now_eastern_text()}  run={run.run_id}  honest={run.honest}",
        "Sort is vs-ask (model fair minus ask). Not P(ITM). n/a = not available.",
        "never_auto_trade=true  paper/mock only",
        "",
        f"{'#':>3} {'Und':<6} {'Side':<4} {'Strike':>8} {'Exp':<10} "
        f"{'P(ITM)':<18} {'Fair':>8} {'Ask':>8} {'vsAsk':>8} {'vsMid':>8} {'Rel':>5} Flags",
        "-" * 110,
    ]
    for i, row in enumerate(run.rows, start=1):
        c = row.contract
        ask = "n/a" if c.quote.ask is None else f"{c.quote.ask:.2f}"
        fair = "n/a" if row.model.fair is None else f"{row.model.fair:.2f}"
        flag = row.n_a_reason or ""
        lines.append(
            f"{i:3d} {c.underlying:<6} {c.contract_type.value:<4} {c.strike:8.2f} "
            f"{c.expiry.isoformat():<10} {_fmt_p(row):<18} {fair:>8} {ask:>8} "
            f"{_fmt_edge(row.vs_ask):>8} {_fmt_edge(row.vs_mid):>8} "
            f"{row.model.reliability:5.2f} {flag}"
        )
    lines += [
        "",
        "Column index",
        "  #       Rank by vs-ask (missing last). Not the highest P(ITM).",
        "  P(ITM)  Chance the option finishes in the money; [low-high] is this snapshot.",
        "  Fair    Model premium (provisional MC). Honest path may be n/a if vol missing.",
        "  vsAsk   Fair minus ask. Ticket bar this week is 0.03 (dollars of premium).",
        "  n/a     No real market, size floor, wide spread, or unconstrained model.",
        "  Note    Observation only. The system never auto-trades.",
    ]
    return "\n".join(lines)


def format_html(run: FieldRun) -> str:
    body = format_table(run).replace("&", "&amp;").replace("<", "&lt;")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{run.field_id}</title></head>"
        f"<body><pre>{body}</pre></body></html>"
    )


def export_table(run: FieldRun) -> dict:
    root = package_root() / EXPORT_DIR
    root.mkdir(parents=True, exist_ok=True)
    stamp = filename_stamp()
    base = root / f"{run.field_id}_{stamp}_{run.run_id}"
    text = format_table(run)
    txt = base.with_suffix(".txt")
    html = base.with_suffix(".html")
    pdf = base.with_suffix(".pdf")
    txt.write_text(text, encoding="utf-8")
    html.write_text(format_html(run), encoding="utf-8")
    _write_pdf(pdf, f"Options field {run.field_id}", text)
    return {"txt": str(txt), "html": str(html), "pdf": str(pdf)}


def _write_pdf(path: Path, title: str, text: str) -> None:
    from fpdf import FPDF

    pdf = FPDF(orientation="L", format="Letter")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Courier", size=7)

    def ascii_line(value: str) -> str:
        cleaned = (
            value.replace("\u2014", "-")
            .replace("\u2013", "-")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u2022", "*")
        )
        return cleaned.encode("latin-1", "replace").decode("latin-1")[:120]

    pdf.cell(0, 5, ascii_line(title), new_x="LMARGIN", new_y="NEXT")
    for line in text.splitlines() or [" "]:
        pdf.cell(0, 3.6, ascii_line(line) or " ", new_x="LMARGIN", new_y="NEXT")
    pdf.output(str(path))
