from pathlib import Path

from src.analytics.kpi import compute_kpi_summary


def test_compute_kpi_summary(tmp_path: Path) -> None:
    sample = tmp_path / "sample.csv"
    sample.write_text(
        "campaign_name,spend,impressions,clicks,actions.purchase,action_values.purchase\n"
        "Campaign A,100,10000,100,5,250\n"
        "Campaign A,50,4000,40,2,100\n"
        "Campaign B,80,7000,70,1,60\n",
        encoding="utf-8",
    )

    summary = compute_kpi_summary(sample)
    assert summary["row_count"] == 3
    assert float(summary["totals"]["spend"]) == 230.0
    assert len(summary["entities"]) == 2
