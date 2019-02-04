from scripts.generate_vars import get_variables, write_development, write_production


def startup_development():
    write_development(get_variables())


def startup_production():
    write_production(get_variables())
