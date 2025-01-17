import requests
from deadlockApi.models.hero import Hero
from deadlockApi.models.match import Welcome, MatchInfo, Player, Objective, DamageMatrix, Stat
async def matches(match_id):
    url = f"https://data.deadlock-api.com/v1/matches/{match_id}/metadata"

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        match_info = MatchInfo(
            duration_s=json_data["match_info"]["duration_s"],
            match_outcome=json_data["match_info"]["match_outcome"],
            winning_team=json_data["match_info"]["winning_team"],
            players=[
                Player(
                    **{
                        **player,
                        "stats": [Stat(**stat) for stat in player["stats"]],  # Преобразуем stats
                    }
                )
                for player in json_data["match_info"]["players"]
            ],
            start_time=json_data["match_info"]["start_time"],
            match_id=json_data["match_info"]["match_id"],
            game_mode=json_data["match_info"]["game_mode"],
            match_mode=json_data["match_info"]["match_mode"],
            objectives=[Objective(**obj) for obj in json_data["match_info"]["objectives"]],
            damage_matrix=DamageMatrix(**json_data["match_info"]["damage_matrix"]),
            match_pauses=[],
            custom_user_stats=[],
            objectives_mask_team0=json_data["match_info"]["objectives_mask_team0"],
            objectives_mask_team1=json_data["match_info"]["objectives_mask_team1"],
            mid_boss=[],
            is_high_skill_range_parties=False,
            low_pri_pool=False,
            new_player_pool=False,
            average_badge_team0=0,
            average_badge_team1=0,
        )

        matchData = Welcome(match_info=match_info)
        return matchData