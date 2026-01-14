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

---

## Results

### Model Comparison

Using **ACT balance MAE** as the primary metric (with TES mean MAE as secondary), models were compared against the human rater.

| Model           | ACT Balance MAE | Spearman ρ (ACT) | TES Mean MAE |
| --------------- | --------------: | ---------------: | -----------: |
| **gpt-4o-mini** |        **6.87** |             0.38 |         0.95 |
| gpt-4o          |            7.80 |         **0.52** |     **0.60** |
| gpt-5.2         |           22.52 |             0.41 |         1.58 |
| gpt-5.1         |           23.76 |             0.49 |         1.22 |

### Interpretation

* **gpt-4o-mini** achieved the lowest ACT balance MAE (6.87), corresponding to an average deviation of ~19% of the full ACT balance range (72 points), making it the closest in absolute terms to human supervisory judgment.
* **gpt-4o** showed the strongest rank-order agreement on ACT balance (Spearman ρ = 0.52) and the lowest TES mean MAE (0.60), indicating particularly strong performance on empathy-related judgments.
* **gpt-5.2** performed substantially worse than GPT-4-class models on ACT balance (MAE = 22.52), despite moderate rank correlation, suggesting larger systematic deviations from human scoring.
* **gpt-5.1** showed similarly high error on ACT balance and is not competitive for this task.

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

Based on the primary evaluation metric (ACT balance MAE), **gpt-4o-mini** is the clear winner. It achieved an ACT balance MAE of **6.87**, corresponding to an average deviation of approximately **19% of the full ACT balance scale** (72 points). This indicates the closest absolute alignment with human supervisory judgment.

Although **gpt-4o** demonstrated stronger rank-order agreement on ACT balance (Spearman ρ = **0.52**) and the lowest TES mean MAE (**0.60**), its higher ACT balance MAE (**7.80**) indicates slightly less accurate calibration of ACT fidelity compared to gpt-4o-mini.

By contrast, **gpt-5.2** showed substantially worse absolute agreement on ACT fidelity (ACT balance MAE = **22.52**, ~31% of the full scale). While its Spearman correlation (ρ = **0.41**) suggests moderate preservation of relative ordering, the magnitude of its errors indicates systematic miscalibration relative to the human rater. As a result, **gpt-5.2 cannot be considered a competitive alternative** for ACT-FM scoring in this dataset. **gpt-5.1** performed similarly poorly and is likewise unsuitable.

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
