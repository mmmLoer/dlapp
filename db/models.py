import json

class Team:
    def __init__(self, team_id, team_name, team_tag, team_caps, approved_ids, teamlist_id):
        self.team_id = team_id
        self.team_name = team_name
        self.team_tag = team_tag
        self.team_caps = team_caps
        self.approved_ids = approved_ids
        self.teamlist_id = teamlist_id

class Teamlist:
    def __init__(self, tournament, name, count_main, count_vip, count_reserve, start_value, top_text,
                 google_sheets_id, bottom_text, date, teams_main, teams_reserve, cap_chat_id,
                 reserve_chat_id, teamlist_chat_id, cap_role_id, reserve_role_id, registration_chat_id,
                 teamlist_message_id, winners_count, stage, status_code, games):
        self.tournament = tournament
        self.name = name
        self.count_main = count_main
        self.count_vip = count_vip
        self.count_reserve = count_reserve
        self.start_value = start_value
        self.top_text = top_text
        self.google_sheets_id = google_sheets_id
        self.bottom_text = bottom_text
        self.date = date
        self.teams_main = teams_main
        self.teams_reserve = teams_reserve
        self.cap_chat_id = cap_chat_id
        self.reserve_chat_id = reserve_chat_id
        self.teamlist_chat_id = teamlist_chat_id
        self.cap_role_id = cap_role_id
        self.reserve_role_id = reserve_role_id
        self.registration_chat_id = registration_chat_id
        self.teamlist_message_id = teamlist_message_id
        self.winners_count = winners_count
        self.stage = stage
        self.status_code = status_code
        self.games = games

class ApprovedSubscriber:
    def __init__(self, team_id, telegram_name, telegram_id, date_approved):
        self.team_id = team_id
        self.telegram_name = telegram_name
        self.telegram_id = telegram_id
        self.date_approved = date_approved

class BannedTeam:
    def __init__(self, team_name, tournament_ids, date_banned, date_out_banned, tournament_banned,
                 reason_ban, proofs):
        self.team_name = team_name
        self.tournament_ids = tournament_ids
        self.date_banned = date_banned
        self.date_out_banned = date_out_banned
        self.tournament_banned = tournament_banned
        self.reason_ban = reason_ban
        self.proofs = proofs

class Tournament:
    def __init__(self, tournament_name, tournament_start_date, tournament_end_date,
                 teamlist_id, prizepool, server_id, admin_channel_id, admin_id):
        self.tournament_name = tournament_name
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.teamlist_id = teamlist_id
        self.prizepool = prizepool
        self.server_id = server_id
        self.admin_channel_id = admin_channel_id
        self.admin_id = admin_id
