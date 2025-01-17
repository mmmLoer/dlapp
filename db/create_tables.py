from database import MySQLDatabase

def create_tables():
    db = MySQLDatabase(host="localhost", user="root", password="Vfn21450", database="shop_db")

    team_columns = {
        "id": "BIGINT AUTO_INCREMENT PRIMARY KEY",
        "team_name": "VARCHAR(255)",
        "team_tag": "VARCHAR(50)",
        "team_caps": "TEXT",
        "approved_tg": "TEXT",
        "approved_yt": "TEXT",
        "approved_tt": "TEXT",
        "approved_inst": "TEXT",
        "teamlist_id": "BIGINT",
        "players_nickname": "TEXT",
        "players_id": "TEXT"
    }

    teamlist_columns = {
        "id": "BIGINT AUTO_INCREMENT PRIMARY KEY",
        "tournament": "BIGINT",
        "name": "VARCHAR(255)",
        "count_main": "BIGINT",
        "count_vip": "BIGINT",
        "count_reserve": "BIGINT",
        "start_value": "BIGINT",
        "top_text": "TEXT",
        "google_sheets_id": "VARCHAR(255)",
        "bottom_text": "TEXT",
        "date": "DATE",
        "teams_main": "TEXT",
        "teams_reserve": "TEXT",
        "cap_chat_id": "BIGINT",
        "reserve_chat_id": "BIGINT",
        "teamlist_chat_id": "BIGINT",
        "cap_role_id": "BIGINT",
        "reserve_role_id": "BIGINT",
        "registration_chat_id": "BIGINT",
        "teamlist_message_id": "BIGINT",
        "winners_count": "BIGINT",
        "stage": "BIGINT",
        "status_code": "BIGINT",
        "games": "BIGINT"
    }

    banned_teams_columns = {
        "id": "BIGINT AUTO_INCREMENT PRIMARY KEY",
        "team_name": "VARCHAR(255)",
        "team_tag": "VARCHAR(50)",
        "team_caps": "TEXT",
        "approved_tg": "TEXT",
        "approved_yt": "TEXT",
        "approved_tt": "TEXT",
        "approved_inst": "TEXT",
        "players_nickname": "TEXT",
        "players_id": "TEXT",
        "tournament_ids": "TEXT",
        "date_banned": "DATE",
        "date_out_banned": "DATE",
        "tournament_banned": "VARCHAR(255)",
        "reason_ban": "BIGINT",
        "proofs": "TEXT"
    }

    tournament_columns = {
        "id": "BIGINT AUTO_INCREMENT PRIMARY KEY",
        "tournament_name": "VARCHAR(255)",
        "tournament_start_date": "DATE",
        "tournament_end_date": "DATE",
        "teamlist_id": "TEXT",
        "prizepool": "BIGINT",
        "server_id": "BIGINT",
        "admin_channel_id": "BIGINT",
        "admin_id": "BIGINT",
        "tg_sponsors": "TEXT",
        "yt_sponsors": "TEXT",
        "tt_sponsors": "TEXT",
        "inst_sponsors": "TEXT",
        "sponsors": "TINYINT",
        "rosters" : "TINYINT"
    }
    proofs_columns = {
        "tournament_id": "BIGINT",
        "telegram_id" : "BIGINT",
        "teamname": "TEXT"
    }
    # db.create_table("Teams", team_columns)
    # db.create_table("teamlists", teamlist_columns)
    # db.create_table("Banned_teams", banned_teams_columns)
    db.create_table("proofs_telegram", proofs_columns)

if __name__ == "__main__":
    create_tables()
