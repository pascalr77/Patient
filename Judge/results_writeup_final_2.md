# Evaluation of Language Models for ACT-FM and TES Rating

## Overview

This experiment evaluates how well large language models can reproduce **human supervisory ratings** of psychotherapy transcripts using:

* the **Acceptance and Commitment Therapy Fidelity Measure (ACT-FM)**, and
* the **Therapist Empathy Scale (TES)**.

The goal is not to assess clinical effectiveness, but to test whether models can approximate the **judgment of a trained ACT supervisor** when scoring transcripts.

---

## Dataset

* **49 psychotherapy transcripts**
* **One human rater** with ACT-FM and TES expertise
* For each transcript:

  * 25 ACT-FM item ratings (0–3)
  * 9 TES item ratings (1–7)

Four models were evaluated:

* **gpt-4o-mini**
* **gpt-4o**
* **gpt-5.1**
* **gpt-5.2**

Each model rated each transcript **once** (temperature = 0.1, deterministic setting).

---

## ACT-FM Scoring Procedure

### Item Grouping

ACT-FM items were grouped following the official ACT-FM structure:

* **Therapist Stance** (items 1–7)
* **Open Response Style** (items 8–13)
* **Aware Response Style** (items 14–19)
* **Engaged Response Style** (items 20–25)

Each category contains **ACT-consistent** and **ACT-inconsistent** items.

### Section Scores (0–9)

* Therapist Stance (consistent) has **4 items**, so its sum was scaled:

  (item₁ + item₂ + item₃ + item₄) / 4 × 3

* All other sections consist of **3 items** and were summed directly.

### Total Scores (0–36)

* **Total ACT Consistency** = sum of the four consistent section scores
* **Total ACT Inconsistency** = sum of the four inconsistent section scores

### ACT Balance Score

The primary ACT outcome is the **ACT balance score**:

ACT Balance = Total Consistency − Total Inconsistency

This produces a continuous score in the range **[−36, +36]**, capturing the *degree* of ACT fidelity.

---

## TES Scoring

For TES, we computed:

* **TES Mean Score**: the mean of the 9 TES items (range 1–7)

This reflects overall therapist empathy as perceived from the transcript.

---

## Evaluation Metrics

### ACT Valid Accuracy

ACT valid accuracy is defined as the proportion of transcripts for which the model’s binary ACT validity decision matches the human reference.

A transcript is considered **ACT valid** if the ACT balance score is positive:

ACT_valid = 1 if (Total Consistency − Total Inconsistency) > 0, otherwise 0.

**Interpretation in this context**:

* ACT valid accuracy reflects how often a model agrees with the human rater on this coarse validity threshold.
* Because all transcripts in this dataset are ACT valid according to the human rater, this metric effectively measures how often a model **does not incorrectly classify a valid transcript as invalid**.

Higher accuracy indicates fewer false invalid classifications relative to the human supervisor.


### Mean Absolute Error (MAE)

For a set of *n* transcripts, MAE is defined as:

MAE = (1 / n) · Σ | yᵢ − ŷᵢ |

where:

* yᵢ is the human reference score
* ŷᵢ is the model-predicted score

**Interpretation in this context**:

* ACT balance scores span **72 points** (−36 to +36).
* An ACT balance MAE of **6–7** corresponds to an average deviation of ~18–20% of the full scale.

Lower MAE indicates closer numerical alignment with human supervision.

---

### Spearman Rank Correlation (ρ)

Spearman’s rho measures rank-order agreement:

ρ = 1 − [6 · Σ dᵢ²] / [n (n² − 1)]

It evaluates whether models preserve the **relative ordering** of transcripts from low to high ACT fidelity.

**Note on p-values**: Spearman’s correlation test reports a p-value for the null hypothesis that the true rank correlation is zero. In this study, that hypothesis is not substantively informative: every model is explicitly prompted to approximate the same human rating process, and the evaluation dataset is fixed (49 transcripts) rather than sampled from a well-defined population in a way that supports inferential generalization. As a result, Spearman p-values primarily reflect sample size and the presence of any monotonic association with the human rater, not whether one model is meaningfully better than another. We therefore report ρ as an effect size describing rank-order agreement, while relying on absolute error metrics (MAE) for primary model comparison.

---

## Results

### Model Comparison

Using **ACT balance MAE** as the primary metric (with TES mean MAE as secondary), models were compared against the human rater.

| Model           | ACT Valid Accuracy | ACT Balance MAE | Spearman ρ (ACT) | Spearman p (ACT) | TES Mean MAE |
| --------------- | -----------------: | --------------: | ---------------: | ---------------: | -----------: |
| **gpt-4o-mini** |                1.0 |        **6.12** |             0.42 |           0.0026 |         1.13 |
| gpt-4o          |                1.0 |            9.29 |             0.35 |            0.014 |         0.80 |
| gpt-5.2         |               0.73 |           24.46 |             0.37 |             0.01 |     **1.86** |
| gpt-5.1         |               0.59 |           24.78 |         **0.49** |           0.0003 |         1.40 |

### Interpretation

* **gpt-4o-mini** achieved the lowest ACT balance MAE (6.12), corresponding to an average deviation of ~17% of the full ACT balance range (72 points), making it the closest in absolute terms to human supervisory judgment. It also achieved perfect ACT validity accuracy (1.0).

* **gpt-4o** showed higher absolute error on ACT balance (MAE = 9.29), but maintained perfect ACT validity accuracy and relatively strong performance on TES (TES mean MAE = 0.80).

* **gpt-5.2** and **gpt-5.1** performed substantially worse on ACT fidelity, with ACT balance MAEs above 24 and notably lower ACT validity accuracy (0.73 and 0.59, respectively), indicating frequent disagreement with the human supervisory decision.

* Although **gpt-5.1** achieved the highest rank-order agreement on ACT balance (Spearman ρ = 0.49), this did not translate into accurate calibration, highlighting that rank correlation alone is insufficient for reliable ACT-FM supervision.

---

## Hardest-to-Rate Items

Item-level analysis shows that the most difficult ACT-FM items for all models involve **experiential and self-as-context processes**, including:

* Helping clients experience separation from psychological content (self-as-context)
* Noticing subtle attentional shifts away from the present moment
* Distinguishing thoughts from events in a functional, non-conceptual way

Similarly, the hardest TES items involve **attunement and acceptance**, which rely on subtle timing and tone not fully captured in text.

---

## Final Model Selection

**Preferred model: gpt-4o-mini**

Based on the primary evaluation metric (ACT balance MAE), **gpt-4o-mini** is the strongest overall model. It achieved the **lowest ACT balance MAE (6.12)**, corresponding to an average deviation of approximately **17% of the full ACT balance scale (72 points)**, indicating the closest absolute alignment with human supervisory judgment. It also achieved perfect ACT validity accuracy (1.0).

Although **gpt-4o** showed moderate rank-order agreement on ACT balance (Spearman ρ = 0.35) and relatively strong performance on TES (TES mean MAE = 0.80), its higher ACT balance MAE (9.29) indicates less accurate calibration of ACT fidelity compared to gpt-4o-mini.

By contrast, **gpt-5.2** and **gpt-5.1** exhibited substantially worse absolute agreement on ACT fidelity, with ACT balance MAEs above 24 and reduced ACT validity accuracy (0.73 and 0.59, respectively). While gpt-5.1 achieved the highest rank-order correlation (Spearman ρ = 0.49), this did not translate into accurate calibration, underscoring that rank correlation alone is insufficient for reliable ACT-FM supervision.

Overall, these results indicate that **GPT-4-class models**, and **gpt-4o-mini** in particular, are best suited for automated ACT-FM scoring in this dataset.

---

## Hardest-to-Rate Items (Item-Level Analysis)

Item-level error analysis identified a subset of ACT-FM and TES items that were consistently difficult for all models. These items require fine-grained interpretation of *function*, *process*, and *moment-to-moment experiential stance*, rather than surface-level content.

### ACT-FM Items

The following ACT-FM items exhibited the highest average MAE across models:

* **Item 16 (Aware Response Style – Consistent):** *Therapist helps the client to experience that they are bigger than their psychological experiences.*
  **Interpretation challenge:** Models often confuse self-as-context with reassurance or cognitive reframing. Incorrect ratings typically reflect treating distancing language as ACT-consistent even when it functions to suppress or control experience.

* **Item 8 (Open Response Style – Consistent):** *Therapist helps the client notice thoughts as separate experiences from the events they describe.*
  **Interpretation challenge:** Models may over-score generic reflective statements without clear experiential defusion, mistaking intellectual insight for functional separation of thought and event.

* **Item 15 (Aware Response Style – Consistent):** *Therapist helps the client notice stimuli that hook them away from the present moment.*
  **Interpretation challenge:** Subtle attentional shifts are often implicit. Models struggle to detect whether attention is being experientially tracked versus merely discussed at a conceptual level.

* **Item 3 (Therapist Stance – Consistent):** *Therapist conveys that it is natural to experience painful thoughts and feelings.*
  **Interpretation challenge:** Models may miss normalization conveyed through tone or pacing, or incorrectly credit explicit validation that actually functions as reassurance.

* **Item 4 (Therapist Stance – Consistent):** *Therapist demonstrates a willingness to sit with painful thoughts and feelings.*
  **Interpretation challenge:** Willingness is often expressed through restraint and silence rather than explicit statements, which models have difficulty inferring from text alone.

### TES Items

The most difficult TES items were:

* **TES Item 5:** *Attunement to the client’s inner world.*
  **Interpretation challenge:** Accurate scoring requires sensitivity to timing, selectivity, and emotional precision—features that are attenuated or ambiguous in text-only transcripts.

* **TES Item 8:** *Acceptance of the client’s feelings and inner experiences.*
  **Interpretation challenge:** Models may overestimate acceptance when empathy is verbally expressed but functionally shifts the client away from difficult material.

* **TES Item 6:** *Understanding the client’s cognitive framework.*
  **Interpretation challenge:** Capturing the client’s internal logic over multiple turns requires maintaining a coherent mental model of the client’s narrative, which remains challenging for automated raters.

---

## Summary

Overall, this evaluation demonstrates that large language models can approximate ACT-FM and TES ratings with **moderate accuracy**, but performance varies substantially by model and by item type. Absolute agreement (MAE) and rank agreement (Spearman ρ) capture complementary but distinct aspects of supervisory judgment. Among the evaluated models, **gpt-4o-mini** provides the most reliable and well-calibrated approximation of human ACT supervisory ratings, while newer models such as **gpt-5.2** do not yet offer improvements for this specific evaluative task.
