# -*- coding:utf-8 -*-

from fastapi import HTTPException

from cookie import suno_auth


def get_token():
    token = suno_auth.get_token()
    if not token:
        raise HTTPException(
            status_code=503,
            detail="Suno token not available. Railway 환경 변수 COOKIE, SESSION_ID 설정 및 Suno 로그인 쿠키 갱신 필요.",
        )
    try:
        yield token
    finally:
        pass
