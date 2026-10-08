"""Package verified week 1 deliverables and evidence; exclude credentials."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "README.md", ".gitignore",
    "docs/week-1/00-plan.md", "docs/week-1/01-services-and-requirements.md",
    "docs/week-1/02-architecture.md", "docs/week-1/03-foundation-runbook.md",
    "docs/week-1/04-evidence-and-review.md", "docs/week-1/05-local-checks.md",
    "docs/week-1/worklog.csv", "docs/week-1/06-live-session.md",
    "docs/week-1/07-deployment-record.md",
    "docs/diagrams/architecture.mmd", "docs/diagrams/architecture.svg", "docs/diagrams/architecture.png",
    "infra/week1-foundation.yaml", "scripts/validate_week1.py",
    "scripts/check-aws-session.ps1", "scripts/deploy-week1.ps1",
    "scripts/render-architecture.py", "scripts/package-week1.py",
    "evidence/week-1/README.md", "evidence/week-1/01-lab-session-ready.jpg",
    "evidence/week-1/02-stack-complete.jpg",
    "evidence/week-1/03-network-check.jpg",
    "evidence/week-1/04-s3-private.jpg",
]
missing = [name for name in FILES if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"Missing files: {missing}")
destination = ROOT / "dist" / "week1-submission.zip"
destination.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
    for name in FILES:
        archive.write(ROOT / name, arcname=name)
with ZipFile(destination) as archive:
    if archive.testzip() is not None:
        raise SystemExit("Archive integrity check failed")
print(f"Packaged {len(FILES)} week 1 files: {destination}")
