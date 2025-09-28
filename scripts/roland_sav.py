"""Command line utility for managing Roland Assistance SAV cases.

This script provides a minimal in-house tool for technicians or support staff
who handle Roland devices.  It keeps track of customer requests in a simple
JSON file that can be synced via Git.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


DEFAULT_DATA_FILE = Path("sav_cases.json")


@dataclass
class ServiceCase:
    """Represents a service-after-sale (SAV) case."""

    case_id: int
    customer_name: str
    contact_email: str
    product_model: str
    serial_number: str
    issue_description: str
    status: str = "open"
    created_at: str = datetime.utcnow().isoformat()
    updated_at: str = datetime.utcnow().isoformat()
    resolution_notes: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ServiceCase":
        return cls(**data)

    def update_status(self, new_status: str, notes: Optional[str] = None) -> None:
        self.status = new_status
        if notes is not None:
            self.resolution_notes = notes
        self.updated_at = datetime.utcnow().isoformat()


class CaseRepository:
    """Simple JSON-backed persistence layer."""

    def __init__(self, file_path: Path = DEFAULT_DATA_FILE) -> None:
        self.file_path = file_path

    def load(self) -> List[ServiceCase]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as fp:
            raw_cases = json.load(fp)
        return [ServiceCase.from_dict(item) for item in raw_cases]

    def save(self, cases: List[ServiceCase]) -> None:
        data = [asdict(case) for case in cases]
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)


def _create_case_id(cases: List[ServiceCase]) -> int:
    if not cases:
        return 1
    return max(case.case_id for case in cases) + 1


def handle_init(repo: CaseRepository) -> None:
    if repo.file_path.exists():
        print(f"Datenbestand existiert bereits unter {repo.file_path}.")
        return
    repo.save([])
    print(f"Neue SAV-Datenbank erstellt: {repo.file_path}")


def handle_add(args: argparse.Namespace, repo: CaseRepository) -> None:
    cases = repo.load()
    new_case = ServiceCase(
        case_id=_create_case_id(cases),
        customer_name=args.customer_name,
        contact_email=args.contact_email,
        product_model=args.product_model,
        serial_number=args.serial_number,
        issue_description=args.issue_description,
    )
    cases.append(new_case)
    repo.save(cases)
    print(f"Fall #{new_case.case_id} erfolgreich angelegt.")


def handle_list(args: argparse.Namespace, repo: CaseRepository) -> None:
    cases = repo.load()
    filtered_cases = [case for case in cases if args.status in (None, case.status)]
    if not filtered_cases:
        status_info = f" mit Status '{args.status}'" if args.status else ""
        print(f"Keine Fälle{status_info} gefunden.")
        return

    print(
        f"\n{'ID':<4} {'Status':<12} {'Kunde':<20} {'Produkt':<15} {'Aktualisiert':<25}"
    )
    print("-" * 85)
    for case in filtered_cases:
        print(
            f"{case.case_id:<4} {case.status:<12} {case.customer_name:<20} "
            f"{case.product_model:<15} {case.updated_at:<25}"
        )


def handle_update(args: argparse.Namespace, repo: CaseRepository) -> None:
    cases = repo.load()
    for case in cases:
        if case.case_id == args.case_id:
            case.update_status(args.status, notes=args.resolution_notes)
            repo.save(cases)
            print(f"Fall #{case.case_id} aktualisiert (Status: {case.status}).")
            return
    print(f"Kein Fall mit der ID {args.case_id} gefunden.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Werkzeug zum Verwalten von Roland Assistance SAV Vorgängen.",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="Pfad zur JSON-Datei, die die Fälle speichert (Standard: sav_cases.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Erstellt eine leere Datenbankdatei")
    init_parser.set_defaults(func=handle_init)

    add_parser = subparsers.add_parser("add", help="Legt einen neuen Support-Fall an")
    add_parser.add_argument("customer_name", help="Name des Kunden/der Kundin")
    add_parser.add_argument("contact_email", help="Kontakt-E-Mail")
    add_parser.add_argument("product_model", help="Roland Produktmodell")
    add_parser.add_argument("serial_number", help="Seriennummer des Produkts")
    add_parser.add_argument("issue_description", help="Kurzbeschreibung des Problems")
    add_parser.set_defaults(func=handle_add)

    list_parser = subparsers.add_parser(
        "list", help="Listet bekannte Fälle auf, optional gefiltert nach Status"
    )
    list_parser.add_argument(
        "--status",
        help="Statusfilter (z.B. open, in_progress, closed)",
    )
    list_parser.set_defaults(func=handle_list)

    update_parser = subparsers.add_parser("update", help="Aktualisiert den Status eines Falls")
    update_parser.add_argument("case_id", type=int, help="ID des Falls")
    update_parser.add_argument("status", help="Neuer Status")
    update_parser.add_argument(
        "--resolution-notes",
        help="Notizen zur Lösung oder zum aktuellen Stand",
    )
    update_parser.set_defaults(func=handle_update)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = CaseRepository(file_path=args.data_file)
    args.func(args, repo)


if __name__ == "__main__":  # pragma: no cover
    main()
