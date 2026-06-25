"""
This page studies bookmaker's calibration
"""

import streamlit as st
import pandas as pd

st.title("Bookmaker Calibration study")
st.subheader("Understanding whether bookmaker probabilities match reality")

st.divider()

# Section 1: Problem Setup
st.text("This study evaluates whether bookmaker probabilities are calibrated. A calibrated bookmaker assigning 70% probability to an outcome should see that outcome occur approximately 70% of the time.")


st.header("1. Problem Setup")

st.write("""
Our objective is to evaluate whether bookmaker probabilities are meaningful
representations of uncertainty.

For every football match, a bookmaker provides a probability distribution over
three possible outcomes:

- Home Win (H)
- Draw (D)
- Away Win (A)
""")

st.write("We denote the bookmaker prediction by:")

st.latex(r"\hat{p} = (\hat{p}_H,\hat{p}_D,\hat{p}_A)")

st.write("where")

st.latex(r"\hat{p}_H+\hat{p}_D+\hat{p}_A=1")

st.info("""
The hat notation indicates a prediction.

These values represent the bookmaker's beliefs before the match is played.
""")

st.subheader("Example")

st.latex(r"\hat{p}=(0.60,0.25,0.15)")

example_probs = pd.DataFrame({
    "Outcome": ["Home Win", "Draw", "Away Win"],
    "Probability": ["60%", "25%", "15%"]
})

st.dataframe(
    example_probs,
    hide_index=True,
    use_container_width=True
)

st.subheader("Observed Outcome")

st.write("""
After the match is played, uncertainty disappears.

Only one outcome occurs.

We represent reality using a one-hot encoded vector:
""")

st.latex(r"y=(y_H,y_D,y_A)")

left, middle, right = st.columns(3)

with left:
    st.latex(r"y=(1,0,0)")
    st.caption("Home Win")

with middle:
    st.latex(r"y=(0,1,0)")
    st.caption("Draw")

with right:
    st.latex(r"y=(0,0,1)")
    st.caption("Away Win")

st.subheader("Prediction vs Reality")

left, right = st.columns(2)

with left:
    st.markdown("#### Prediction")
    st.latex(r"\hat{p}=(0.60,0.25,0.15)")

with right:
    st.markdown("#### Reality")
    st.latex(r"y=(1,0,0)")

st.write("""
Our entire project is about comparing these two objects:

- Predicted probability distribution
- Actual outcome

and measuring how close they are.
""")

st.divider()

st.header("2. Measuring Prediction Error")

st.write("""
The first question we can ask is:

How close was the bookmaker prediction to reality?

A standard metric used for probability forecasts is the Brier Score.
""")

st.latex(
r"""
BS=
(\hat{p}_H-y_H)^2
+
(\hat{p}_D-y_D)^2
+
(\hat{p}_A-y_A)^2
"""
)

st.write("""
The Brier Score measures the squared distance between prediction and reality.

Smaller values indicate better probability forecasts.
""")

st.subheader("Interpreting Brier Scores")

st.write("""
A Brier Score of 0 corresponds to a perfect prediction.

Larger values indicate that probability mass was assigned to outcomes that did
not occur, or that too little probability was assigned to the outcome that did occur.
""")

st.write("""
For a bookmaker, we compute the average Brier Score across all matches:
""")

st.latex(
r"""
\overline{BS}
=
\frac{1}{N}
\sum_{i=1}^{N}
BS_i
"""
)

st.write("""
This allows us to compare bookmakers.

Example:

- Bookmaker A : 0.56
- Bookmaker B : 0.60

Bookmaker A produced probability forecasts that were closer to reality on average.
""")

st.warning("""
A lower average Brier Score does not automatically imply a statistically
significant difference.

Later we will introduce confidence intervals and uncertainty estimates to
determine whether differences between bookmakers are meaningful.
""")

st.divider()

st.header("3. Why Brier Score Is Not Enough")

st.write("""
The Brier Score measures overall forecast quality.

However, it does not answer the question that motivated this project:
""")

st.success("""
When a bookmaker predicts 60%, does the event actually occur 60% of the time?
""")

st.write("""
Two bookmakers may have similar Brier Scores while exhibiting very different
probability behavior.

One bookmaker might systematically overestimate favorites.

Another bookmaker might systematically underestimate them.

The Brier Score alone cannot reveal these patterns.
""")

st.write("""
To study whether probabilities are trustworthy, we need another statistical lens.

This leads us to calibration.
""")

st.divider()

st.header("4. Why We Need Bins")

st.write("""
Calibration investigates the relationship between predicted probabilities and
observed frequencies.

Ideally, we would like to estimate:
""")

st.latex(r"P(y=1 \mid \hat{p}=x)")

st.write("""
Unfortunately, probabilities are continuous.

In practice, almost every match receives a slightly different probability.
""")

example_probs = pd.DataFrame({
    "Predicted Probability": [
        0.58,
        0.61,
        0.63,
        0.59,
        0.64,
        0.57
    ]
})

st.dataframe(
    example_probs,
    hide_index=True,
    use_container_width=True
)

st.write("""
Because probabilities rarely repeat exactly, we cannot directly estimate
long-run frequencies.

Instead, we group nearby probabilities together.
""")

st.subheader("Fixed Width Bins")

bins_df = pd.DataFrame({
    "Bin": [
        "0.0 - 0.1",
        "0.1 - 0.2",
        "0.2 - 0.3",
        "0.3 - 0.4",
        "0.4 - 0.5",
        "0.5 - 0.6",
        "0.6 - 0.7",
        "0.7 - 0.8",
        "0.8 - 0.9",
        "0.9 - 1.0"
    ]
})

st.dataframe(
    bins_df,
    hide_index=True,
    use_container_width=True
)

st.write("""
For example, all probabilities between 60% and 70% can be treated as belonging
to the same group.

Inside each bin we can compute:

- Average predicted probability
- Actual observed frequency

and compare the two.
""")

st.info("""
This is the foundation of calibration analysis.

In the next section we will investigate how bookmaker probabilities are
distributed across these bins and whether the chosen binning strategy is reasonable.
""")

st.divider()

st.header("5. Distribution of Predicted Probabilities")

st.write("""
Before building calibration curves, we need to verify that our binning strategy
is reasonable.

A calibration curve relies on estimating frequencies inside bins.

If some bins contain very few observations, the estimated frequencies become
unstable and unreliable.

Therefore, our first step is to investigate how bookmaker probabilities are
distributed.
""")

st.subheader("Why This Matters")

st.write("""
Suppose we use 10 fixed-width bins:

- 0.0 – 0.1
- 0.1 – 0.2
- ...
- 0.9 – 1.0

If most observations fall into only a few bins, then some calibration estimates
will be based on very small samples.

This introduces noise and can make the calibration curve misleading.
""")

st.success("""
Good calibration analysis requires a reasonable number of observations inside
each bin.
""")

st.divider()

st.subheader("Home Win Probabilities")

st.write("""
We begin by examining the distribution of predicted Home Win probabilities.
""")

