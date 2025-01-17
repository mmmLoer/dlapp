from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


@dataclass
class MatchInfoCustomUserStat:
    name: str
    id: int


@dataclass
class DamageToPlayer:
    target_player_slot: int
    damage: Optional[List[int]] = None


@dataclass
class DamageSource:
    damage_to_players: List[DamageToPlayer]
    source_details_index: int


@dataclass
class DamageDealer:
    dealer_player_slot: int
    damage_sources: List[DamageSource]


class StatType(Enum):
    K_E_TYPE_DAMAGE = "k_eType_Damage"
    K_E_TYPE_HEALING = "k_eType_Healing"
    K_E_TYPE_HEAL_PREVENTED = "k_eType_HealPrevented"
    K_E_TYPE_LETHAL_DAMAGE = "k_eType_LethalDamage"
    K_E_TYPE_MITIGATED = "k_eType_Mitigated"


@dataclass
class SourceDetails:
    stat_type: List[StatType]
    source_name: List[str]


@dataclass
class DamageMatrix:
    damage_dealers: List[DamageDealer]
    sample_time_s: List[int]
    source_details: SourceDetails


@dataclass
class MatchPause:
    game_time_s: int
    pause_duration_s: int
    player_slot: int


class WinningTeam(Enum):
    K_E_CITADEL_LOBBY_TEAM_TEAM0 = "k_ECitadelLobbyTeam_Team0"
    K_E_CITADEL_LOBBY_TEAM_TEAM1 = "k_ECitadelLobbyTeam_Team1"


@dataclass
class MidBoss:
    team_killed: WinningTeam
    team_claimed: WinningTeam
    destroyed_time_s: int


@dataclass
class Objective:
    destroyed_time_s: int
    creep_damage: int
    creep_damage_mitigated: int
    player_damage: int
    player_damage_mitigated: int
    first_damage_time_s: int
    team_objective_id: str
    team: WinningTeam


@dataclass
class AbilityStat:
    ability_id: int
    ability_value: int


@dataclass
class Pos:
    x: float
    y: float
    z: float


@dataclass
class DeathDetail:
    game_time_s: int
    killer_player_slot: int
    death_pos: Pos
    killer_pos: Pos
    death_duration_s: int


@dataclass
class Item:
    game_time_s: int
    item_id: int
    upgrade_id: int
    sold_time_s: int
    flags: int
    imbued_ability_id: int


@dataclass
class Ping:
    ping_type: int
    ping_data: int
    game_time_s: int


@dataclass
class StatCustomUserStat:
    value: int
    id: int


class Source(Enum):
    K_E_ASSISTS = "k_eAssists"
    K_E_BOSSES = "k_eBosses"
    K_E_DENIES = "k_eDenies"
    K_E_LANE_CREEPS = "k_eLaneCreeps"
    K_E_NEUTRALS = "k_eNeutrals"
    K_E_PLAYERS = "k_ePlayers"
    K_E_TEAM_BONUS = "k_eTeamBonus"
    K_E_TREASURE = "k_eTreasure"


@dataclass
class GoldSource:
    source: Source
    gold: int
    kills: Optional[int] = None
    damage: Optional[int] = None
    gold_orbs: Optional[int] = None


@dataclass
class Stat:
    time_stamp_s: int
    net_worth: int
    gold_player: int
    gold_player_orbs: int
    gold_lane_creep_orbs: int
    gold_neutral_creep_orbs: int
    gold_boss: int
    gold_boss_orb: int
    gold_treasure: int
    gold_denied: int
    gold_death_loss: int
    gold_lane_creep: int
    gold_neutral_creep: int
    kills: int
    deaths: int
    assists: int
    creep_kills: int
    neutral_kills: int
    possible_creeps: int
    creep_damage: int
    player_damage: int
    neutral_damage: int
    boss_damage: int
    denies: int
    player_healing: int
    ability_points: int
    self_healing: int
    player_damage_taken: int
    max_health: int
    weapon_power: int
    tech_power: int
    shots_hit: int
    shots_missed: int
    damage_absorbed: int
    absorption_provided: int
    hero_bullets_hit: int
    hero_bullets_hit_crit: int
    heal_prevented: int
    heal_lost: int
    gold_sources: List[GoldSource]
    custom_user_stats: List[StatCustomUserStat]
    damage_mitigated: int
    level: int


@dataclass
class Player:
    account_id: int
    player_slot: int
    items: List[Item]
    stats: List[Stat]
    team: WinningTeam
    kills: int
    deaths: int
    assists: int
    net_worth: int
    hero_id: int
    last_hits: int
    denies: int
    ability_points: int
    party: int
    assigned_lane: int
    level: int
    stats_type_stat: List[float]
    death_details: Optional[List[DeathDetail]] = None
    pings: Optional[List[Ping]] = None
    ability_stats: Optional[List[AbilityStat]] = None


@dataclass
class MatchInfo:
    duration_s: int
    match_outcome: str
    winning_team: WinningTeam
    players: List[Player]
    start_time: int
    match_id: int
    game_mode: str
    match_mode: str
    objectives: List[Objective]
    damage_matrix: DamageMatrix
    match_pauses: List[MatchPause]
    custom_user_stats: List[MatchInfoCustomUserStat]
    objectives_mask_team0: int
    objectives_mask_team1: int
    mid_boss: List[MidBoss]
    is_high_skill_range_parties: bool
    low_pri_pool: bool
    new_player_pool: bool
    average_badge_team0: int
    average_badge_team1: int


@dataclass
class Welcome:
    match_info: MatchInfo
