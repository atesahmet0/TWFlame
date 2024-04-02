def get_current_database() -> str:
    """
    Get current database location
    :return: Path to the .db file as "..../database.db"
    """
    return "accounts.db"


def get_accounts_database_default_table_name():
    """
    Get the default table name for the accounts database
    :return: 
    """
    return "accounts"
