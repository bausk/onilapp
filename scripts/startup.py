from scripts.generate_vars import get_variables, write_development


def startup_development():
    write_development(get_variables('production', 'development'))
