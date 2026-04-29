from db.connection import Database


class ConfigLoader:

    @staticmethod
    def get_all_config():
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT site, key, value FROM config")
        rows = cursor.fetchall()

        config = {}

        for site, key, value in rows:
            if site not in config:
                config[site] = {}
            config[site][key] = value

        cursor.close()
        Database.release_connection(conn)

        return config

    @staticmethod
    def get_value(site, key):
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT value FROM config WHERE site = %s AND key = %s",
            (site, key)
        )
        result = cursor.fetchone()

        cursor.close()
        Database.release_connection(conn)

        return result[0] if result else None

    @staticmethod
    def get_global(key):
        return ConfigLoader.get_value("global", key)

    @staticmethod
    def get_site_config(site):
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT key, value FROM config WHERE site = %s",
            (site,)
        )
        rows = cursor.fetchall()

        site_config = {key: value for key, value in rows}

        cursor.close()
        Database.release_connection(conn)

        return site_config