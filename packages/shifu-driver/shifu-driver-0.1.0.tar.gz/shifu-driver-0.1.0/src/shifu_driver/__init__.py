from flask import Blueprint

driver_bp = Blueprint('driver', __name__)

from .driver import ShifuDriver   # noqa: E402, F401
