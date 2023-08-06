class PageFormatError(Exception):
    """Error related to Page Format"""

    def __init__(self, run_pages):

        pages_type = type(run_pages)

        if pages_type == str:
            if run_pages != "all":
                self.message = (
                    "You passed a non valid string value to the "
                    "`run_pages` variable. In this version, the only "
                    "possible string option for this variable is 'all'."
                )
                super().__init__(self.message)

        elif (pages_type != list) and (pages_type != tuple):
            self.message = (
                "The `run_pages` variable on params.yaml file "
                f"has the type {pages_type}. The required types "
                "for this variable is a string, a list or a tuple."
            )
            super().__init__(self.message)


class DatabaseTypeError(Exception):
    def __init__(self, database):

        if database != "athena" and database != "sqlite":
            self.message = (
                "You passed a non valid string value to the "
                "`database` variable. In this version, the only "
                "possible string options for this variable are "
                "'athena' and 'sqlite'."
            )
            super().__init__(self.message)
