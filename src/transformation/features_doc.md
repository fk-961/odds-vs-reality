# Implied Probabilities and Bookmaker Margin

Bookmakers express their beliefs about a match through odds. For a given outcome, the raw implied probability is computed as:

$$
P = \frac{1}{\text{odds}}
$$

---

For a 3-way football market (Home, Draw, Away), the raw implied probabilities are:

$$
P_H = \frac{1}{H}, \quad
P_D = \frac{1}{D}, \quad
P_A = \frac{1}{A}
$$

---

Unlike true probabilities, these values typically sum to more than 1. The excess probability mass represents the bookmaker's margin (also called overround):

$$
\text{Margin} =
\left(
\frac{1}{H} +
\frac{1}{D} +
\frac{1}{A}
\right) - 1
$$

A margin of 0.05 corresponds to a 5% bookmaker edge.

---

An important limitation is that the margin is observed only at the market level. While the total margin can be calculated, it is not possible to know exactly how it is distributed across the Home, Draw, and Away outcomes. In practice, bookmakers may allocate more margin to specific outcomes depending on bettor behavior, risk management, or market conditions.

---

For this project, we assume that the margin is distributed proportionally across outcomes and use the standard normalization approach to obtain probabilities that sum to 1:

$$
P_H^* = \frac{P_H}{P_H + P_D + P_A}
$$

$$
P_D^* = \frac{P_D}{P_H + P_D + P_A}
$$

$$
P_A^* = \frac{P_A}{P_H + P_D + P_A}
$$

---

These normalized probabilities will be used throughout the project when comparing bookmaker expectations against actual match results.