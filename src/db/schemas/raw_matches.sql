DROP TABLE matches;

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- metadata
    league_division TEXT,
    season TEXT,
    match_date DATE,
    kick_off TIME,

    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,

    -- results
    full_time_home_goals SMALLINT CHECK (full_time_home_goals >= 0),
    full_time_away_goals SMALLINT CHECK (full_time_away_goals >= 0),
    full_time_match_result CHAR(1),

    half_time_home_goals SMALLINT,
    half_time_away_goals SMALLINT,
    half_time_match_result CHAR(1),

    -- match stats
    home_shots SMALLINT,
    away_shots SMALLINT,

    home_shots_on_target SMALLINT,
    away_shots_on_target SMALLINT,

    home_corners SMALLINT,
    away_corners SMALLINT,

    home_fouls SMALLINT,
    away_fouls SMALLINT,

    home_yellow_cards SMALLINT,
    away_yellow_cards SMALLINT,

    home_red_cards SMALLINT,
    away_red_cards SMALLINT,

    -- odds (standard markets)
    bet365_home_odds FLOAT,
    bet365_draw_odds FLOAT,
    bet365_away_odds FLOAT,

    bet365_closing_home_odds FLOAT,
    bet365_closing_draw_odds FLOAT,
    bet365_closing_away_odds FLOAT,

    pinnacle_home_odds FLOAT,
    pinnacle_draw_odds FLOAT,
    pinnacle_away_odds FLOAT,

    pinnacle_closing_home_odds FLOAT,
    pinnacle_closing_draw_odds FLOAT,
    pinnacle_closing_away_odds FLOAT,

    betwin_home_odds FLOAT,
    betwin_draw_odds FLOAT,
    betwin_away_odds FLOAT,

    betwin_closing_home_odds FLOAT,
    betwin_closing_draw_odds FLOAT,
    betwin_closing_away_odds FLOAT,

    -- market aggregates
    market_average_home_odds FLOAT,
    market_average_draw_odds FLOAT,
    market_average_away_odds FLOAT,

    market_average_closing_home_odds FLOAT,
    market_average_closing_draw_odds FLOAT,
    market_average_closing_away_odds FLOAT,

    market_maximum_home_odds FLOAT,
    market_maximum_draw_odds FLOAT,
    market_maximum_away_odds FLOAT,

    market_maximum_closing_home_odds FLOAT,
    market_maximum_closing_draw_odds FLOAT,
    market_maximum_closing_away_odds FLOAT
);