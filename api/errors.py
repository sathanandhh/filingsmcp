"""Map engine errors to HTTP. The body is always {"user_message": <friendly>} so the UI
shows something a non-technical person understands — never a traceback or status code."""
from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
from engine.errors import (
    FilingsMCPError, CompanyNotFoundError, BSEUnavailableError, DownloadError,
    SkillImportError,
)

_STATUS = {
    CompanyNotFoundError: 404,
    BSEUnavailableError: 503,
    DownloadError: 502,
    SkillImportError: 400,
}


def status_for(exc: FilingsMCPError) -> int:
    for cls, code in _STATUS.items():
        if isinstance(exc, cls):
            return code
    return 500


async def filingsmcp_exception_handler(request: Request, exc: FilingsMCPError) -> JSONResponse:
    return JSONResponse(status_code=status_for(exc), content={"user_message": exc.user_message})
