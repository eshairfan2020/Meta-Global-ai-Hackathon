from collections import OrderedDict
from datetime import datetime, timezone
import secrets

from .errors import CaseNotFound
from .schemas import CaseView, VerificationEvent, VerificationStatus

MAX_CASES = 100


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class CaseStore:
    """Temporary in-memory cases. Cleared on backend restart. Stores no raw message text."""

    def __init__(self) -> None:
        self._cases: OrderedDict[str, CaseView] = OrderedDict()

    def create(self, **fields) -> CaseView:
        case = CaseView(case_id=secrets.token_urlsafe(9), created_at=now_iso(), **fields)
        self._cases[case.case_id] = case
        while len(self._cases) > MAX_CASES:
            self._cases.popitem(last=False)
        return case

    def get(self, case_id: str) -> CaseView:
        try:
            return self._cases[case_id]
        except KeyError:
            raise CaseNotFound() from None

    def record(self, case_id: str, status: VerificationStatus) -> CaseView:
        case = self.get(case_id)
        case.verification.events.append(VerificationEvent(status=status, timestamp=now_iso()))
        case.verification.status = status
        return case

    def delete(self, case_id: str) -> None:
        self.get(case_id)
        del self._cases[case_id]
