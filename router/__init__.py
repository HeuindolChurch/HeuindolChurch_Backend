from fastapi import APIRouter

from . import user, account, auth

router = APIRouter()

router.add_api_route('/', account.router)
router.add_api_route('/', auth.router)
router.add_api_route('/', user.router)
