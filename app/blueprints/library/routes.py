from . import library_bp

@library_bp.route("/library")
def library():
    return "Library"
