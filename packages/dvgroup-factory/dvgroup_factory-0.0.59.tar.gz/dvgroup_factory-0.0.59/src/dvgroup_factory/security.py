from fastapi import Path, Request, HTTPException, status
from typing import Optional, List
from fastapi.security import SecurityScopes
import traceback
import json


class SecurityStructure:
    def __init__(self, scopes: Optional[List[str]] = None, tenants: Optional[List[str]] = None):
        self.scopes = scopes or []
        self.scopes_str = " ".join(self.scopes)
        self.tenants = tenants or []
        self.tenants_str = " ".join(self.tenants)

class VerifySecurity:
    def __init__(self, logger, factory, do_auth=None, scope_rules=None):
        self.logger = logger
        consul = factory.consul(new=True)
        self.do_auth = json.loads(consul.kv.get("services/auth-api/do_auth"))["do"]
        self.scope_rules = json.loads(consul.kv.get("services/auth-api/scopes"))
        if do_auth is not None:
            self.do_auth = do_auth
        if scope_rules is not None:
            self.scope_rules = scope_rules

    async def verify_security(self, scopes: SecurityScopes, request: Request, tenant_id: str = Path("")): #user_scopes: Optional[str] = Header([], alias="user_scopes")
        try:
            self.logger.info(f'In scopes = {scopes.scopes}, tenants = {tenant_id}')
            security = SecurityStructure(scopes.scopes, [tenant_id])
            if self.do_auth != 'yes':
                return security
            if not request.auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorised")
            try:
                user_scopes = request.user.scopes
                user_tenants = request.user.tenants
                self.logger.info(f'User scopes = {user_scopes}, tenants = {user_tenants}')
            except Exception as e:
                self.logger.info(f'Error = {traceback.format_exc()}')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
            intersection_scopes = list(set(user_scopes) & set(security.scopes))
            if len(intersection_scopes) == 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing scopes", )
            intersection_tenants = list(set(user_tenants) & set(security.tenants))
            if len(intersection_tenants) == 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing tenants", )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            self.logger.info(f'Error = {traceback.format_exc()}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=traceback.format_exc())
        return SecurityStructure(intersection_scopes, intersection_tenants)

    async def _get_scopes_from_path(self, sec_scopes: SecurityScopes, request: Request):
        method = request.method
        pth = sec_scopes.scopes[0]
        full_pth = f"{method} {pth}"
        #self.logger.info(f'full_pth = {full_pth}')
        scopes = self.scope_rules.get(full_pth, {}).get("scopes", [])
        #self.logger.info(f'scopes = {scopes}')
        return SecurityScopes(scopes)

    async def verify_scopes_from_path(self, sec_scopes: SecurityScopes, request: Request):
        scopes = await self._get_scopes_from_path(sec_scopes, request)
        return await self.verify_scopes(scopes, request)

    async def verify_scopes(self, sec_scopes: SecurityScopes, request: Request):
        try:
            if self.do_auth != 'yes':
                return sec_scopes
            if not request.auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorised")
            self.logger.info(f'sec_scopes.scope_str = {sec_scopes.scope_str}, type = {type(sec_scopes)}')
            try:
                self.logger.info(f'request.user = {request.user}')
                user_scopes = request.user.scopes
            except Exception as e:
                self.logger.info(f'Error = {traceback.format_exc()}')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
            intersection_scopes = list(set(user_scopes) & set(sec_scopes.scopes))
            if len(intersection_scopes) == 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing scopes", )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            self.logger.info(f'err = {traceback.format_exc()}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return intersection_scopes
