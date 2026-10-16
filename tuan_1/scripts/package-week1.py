"""Package verified week 1 deliverables and evidence; exclude credentials."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    "dist/Bao_cao_tuan_1_Learner_Lab_Ops_Dashboard_24110019.docx",
    "README.md", ".gitignore", "docs/data-sources.md", "docs/images/hcmute-logo.png",
    "tuan_1/README.md",
    "tuan_1/docs/00-plan.md", "tuan_1/docs/01-services-and-requirements.md",
    "tuan_1/docs/02-architecture.md", "tuan_1/docs/03-foundation-runbook.md",
    "tuan_1/docs/04-evidence-and-review.md", "tuan_1/docs/05-local-checks.md",
    "tuan_1/docs/worklog.csv", "tuan_1/docs/06-live-session.md",
    "tuan_1/docs/07-deployment-record.md", "tuan_1/docs/08-cloudtrail-audit.md",
    "tuan_1/diagrams/architecture-week1-simple.mmd", "tuan_1/diagrams/architecture-week1-simple.svg",
    "tuan_1/diagrams/architecture-week1-simple.png", "tuan_1/infra/week1-foundation.yaml",
    "tuan_1/scripts/validate_week1.py", "tuan_1/scripts/check-aws-session.ps1",
    "tuan_1/scripts/deploy-week1.ps1", "tuan_1/scripts/render-simple-architecture.py",
    "tuan_1/scripts/build-week1-report.py", "tuan_1/scripts/finalize-week1-report.ps1",
    "tuan_1/scripts/package-week1.py", "tuan_1/evidence/README.md",
    "tuan_1/evidence/01-lab-session-ready.jpg", "tuan_1/evidence/02-stack-complete.jpg",
    "tuan_1/evidence/03-network-check.jpg", "tuan_1/evidence/04-s3-private.jpg",
]
missing = [name for name in FILES if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"Missing files: {missing}")
destination = ROOT / "dist" / "week1-submission.zip"
destination.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
    for name in FILES:
        archive.write(ROOT / name, arcname=name[5:] if name.startswith("dist/") else name)
with ZipFile(destination) as archive:
    if archive.testzip() is not None:
        raise SystemExit("Archive integrity check failed")
print(f"Packaged {len(FILES)} week 1 files: {destination}")
