class ScoringFormat:
    """Stores a set of scoring rules."""
    def __init__(self, 
                 pass_yards_value: float,
                 pass_tds_value: int,
                 pass_ints_value: int,
                 rush_yards_value: float,
                 rush_tds_value: int,
                 receptions_value: float,
                 rec_yards_value: float,
                 rec_tds_value: int,
                 two_point_conversions_value: int,
                 fumble_recovery_td_value: int,
                 fumble_lost_value: int,
                 name: str):
        self.pass_yards_value = pass_yards_value
        self.pass_tds_value = pass_tds_value
        self.pass_ints_value = pass_ints_value
        self.rush_yards_value = rush_yards_value
        self.rush_tds_value = rush_tds_value
        self.receptions_value = receptions_value
        self.rec_yards_value = rec_yards_value
        self.rec_tds_value = rec_tds_value
        self.two_point_conversions_value = two_point_conversions_value
        self.fumble_recovery_td_value = fumble_recovery_td_value
        self.fumble_lost_value = fumble_lost_value
        self.name = name


class StandardScoringFormat(ScoringFormat):
    """Standard scoring format with default values."""
    def __init__(self):
        super().__init__(
            pass_yards_value=0.04,
            pass_tds_value=4,
            pass_ints_value=-2,
            rush_yards_value=0.1,
            rush_tds_value=6,
            receptions_value=0,
            rec_yards_value=0.1,
            rec_tds_value=6,
            two_point_conversions_value=2,
            fumble_recovery_td_value=6,
            fumble_lost_value=-2,
            name="Standard"
        )


class PPRScoringFormat(ScoringFormat):
    """PPR scoring format with default values."""
    def __init__(self):
        super().__init__(
            pass_yards_value=0.04,
            pass_tds_value=4,
            pass_ints_value=-2,
            rush_yards_value=0.1,
            rush_tds_value=6,
            receptions_value=1,
            rec_yards_value=0.1,
            rec_tds_value=6,
            two_point_conversions_value=2,
            fumble_recovery_td_value=6,
            fumble_lost_value=-2,
            name="PPR"
        )

        
# Dict of {column_name: attr_name} for use with the nfl-data-py library
stat_mapping_nfl_py = {
    #PASSING
    'passing_yards' : 'pass_yards_value',
    'passing_tds' : 'pass_tds_value',
    'interceptions' : 'pass_ints_value',
    #RUSHING
    'rushing_yards' : 'rush_yards_value',
    'rushing_tds': 'rush_tds_value',
    #RECEIVING
    'receptions' : 'receptions_value',
    'receiving_yards' : 'rec_yards_value',
    'receiving_tds' : 'rec_tds_value',
    #MISC
    'sack_fumbles_lost' : 'fumble_lost_value', # This data source distinguishes between different kinds of fumbles
    'rushing_fumbles_lost' : 'fumble_lost_value',
    'receiving_fumbles_lost' : 'fumble_lost_value',
    'passing_2pt_conversions' : 'two_point_conversions_value', # Same for 2pt conversions
    'rushing_2pt_conversions' : 'two_point_conversions_value',
    'receiving_2pt_conversions' : 'two_point_conversions_value',    
}


def calculate_fantasy_points(
    stats_row: pd.Series, 
    scoring_format: ScoringFormat, 
    stat_mapping:dict, 
    debug=False) -> float:
    """Calculates the total points scored by one row of stats. """
    total_points = 0.0
    for column, scoring_attribute in stat_mapping.items():
        if column in stats_row and hasattr(scoring_format, scoring_attribute):
            total_points += stats_row[column] * getattr(scoring_format, scoring_attribute)
            if debug == True:
                print(f"{column} : {stats_row[column]}, {scoring_attribute} : {getattr(scoring_format, scoring_attribute)}")
    return total_points
    
    
    def calculate_fantasy_points_by_category(
    stats_row: pd.Series, 
    scoring_format: ScoringFormat, 
    stat_mapping:dict, 
    debug=False) -> dict:
    """Calculates the total points scored by one row of stats, returning a dict mapping each scoring category to its respective points. """
    points_by_category = {}
    for column, scoring_attribute in stat_mapping.items():
        if column in stats_row and hasattr(scoring_format, scoring_attribute):
            points_by_category[scoring_attribute] =  stats_row[column] * getattr(scoring_format, scoring_attribute)
            if debug == True:
                print(f"{column} : {stats_row[column]}, {scoring_attribute} : {getattr(scoring_format, scoring_attribute)}")
    return points_by_category