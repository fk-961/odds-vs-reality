# Data Validation Checks

## Overview

The validation pipeline runs after the ingestion step and before any analytics or modeling work.

Its objective is to ensure that the data loaded into the database is:

* Complete
* Consistent
* Conforms to the expected schema
* Respects football-specific business rules

The validation pipeline should generate:

* Terminal summary
* JSON validation report
* Pipeline failure on critical errors

---

# Validation Categories

## 1. Schema Validation

### Objective

Ensure the database schema matches the expected design defined in:

* `schema.sql`
* `mappings.py`

### Checks

* All expected columns exist
* No unexpected columns are present
* SQL data types are correct
* Primary key exists
* Required columns are not nullable

### Severity

**Critical**

Failure should stop the pipeline.

---

## 2. Missing Values Analysis

### Objective

Measure dataset completeness and identify problematic columns.

### Checks

For each column:

* Null count
* Null percentage

Special attention should be paid to:

* `match_date`
* `home_team`
* `away_team`
* `full_time_home_goals`
* `full_time_away_goals`
* `full_time_match_result`

### Severity

* Critical columns → Fail if nulls exist
* Optional columns → Warning only

---

## 3. Value Range Validation

### Objective

Verify that numeric values fall within reasonable ranges.

### Goals

Checks:

* `full_time_home_goals >= 0`
* `full_time_away_goals >= 0`
* `half_time_home_goals >= 0`
* `half_time_away_goals >= 0`

### Match Statistics

Checks:

* Shots >= 0
* Shots on target >= 0
* Corners >= 0
* Fouls >= 0
* Yellow cards >= 0
* Red cards >= 0

### Betting Odds

Checks:

* Odds > 1.0
* Odds < 100.0

### Severity

**Critical**

Failure should stop the pipeline.

---

## 4. Duplicate Detection

### Objective

Ensure matches are not loaded multiple times.

### Duplicate Definition

Potential duplicates are identified using:

* `season`
* `match_date`
* `home_team`
* `away_team`

### Severity

**Critical**

Failure should stop the pipeline.

---

## 5. Match Result Consistency

### Objective

Verify that recorded match results are consistent with the final score.

### Rules

If:

```text
full_time_home_goals > full_time_away_goals
```

then:

```text
full_time_match_result = 'H'
```

If:

```text
full_time_home_goals < full_time_away_goals
```

then:

```text
full_time_match_result = 'A'
```

If:

```text
full_time_home_goals = full_time_away_goals
```

then:

```text
full_time_match_result = 'D'
```

### Severity

**Critical**

Failure should stop the pipeline.

---

## 6. Season Integrity Validation

### Objective

Verify that each season is structurally complete.

### Team Count

Compute:

* Number of unique teams per season

### Match Count Formula

For a complete double round-robin league:

```math
k = n(n - 1)
```

Where:

* `n` = number of teams
* `k` = expected number of matches

Checks:

```text
actual_matches == expected_matches
```

### Severity

* Historical seasons → Critical
* Current season → Warning

---

## 7. Team Participation Validation

### Objective

Verify that every team played the expected number of matches.

### Formula

For a double round-robin league:

```math
2(n - 1)
```

matches per team.

Examples:

* 20 teams → 38 matches
* 18 teams → 34 matches

Checks:

```text
actual_matches == expected_matches
```

for every team in a season.

### Severity

* Historical seasons → Critical
* Current season → Warning