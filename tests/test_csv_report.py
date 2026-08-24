from scripts.csv_report import summarize_csv


def test_summarize_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,score\nAda,90\nGrace,85\nLinus,\n")

    summary = summarize_csv(str(csv_path))

    assert summary["rows"] == 3
    assert summary["columns"]["name"]["non_null"] == 3
    assert summary["columns"]["score"]["non_null"] == 2
    assert summary["columns"]["score"]["mean"] == 87.5
    assert summary["columns"]["score"]["min"] == 85
    assert summary["columns"]["score"]["max"] == 90
