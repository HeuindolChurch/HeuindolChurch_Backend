from fastapi import APIRouter

from . import user, account, auth, initial

router = APIRouter()

router.include_router(account.router, prefix='/account', )
router.include_router(auth.router, prefix='/auth')
router.include_router(user.router, prefix='/user')
router.include_router(initial.router, prefix='/init')
