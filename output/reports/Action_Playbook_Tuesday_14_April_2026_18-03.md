# Weekly Action Playbook

Run ID: `weekly_20260414T123328_08219b1e`

## Proposed Actions (Human Approval Required)

- [PROPOSED] `Audit the conversion value attribution model to determine whether the uniform $2,280 conversion value per campaign reflects actual revenue or a placeholder, and implement dynamic revenue tracking if not already in place.` on `All Campaigns` (confidence 0.90): Identical conversion values across all campaigns ($2,280 each) despite differing spend levels and conversion counts is anomalous and prevents accurate ROAS-based budget allocation decisions.
- [PROPOSED] `Investigate why all campaigns have identical impressions and clicks despite different spend levels, and determine if impression or click caps are artificially constraining performance.` on `All Campaigns` (confidence 0.80): Uniform impressions (45,000) and clicks (660) across campaigns with spend ranging from $495 to $810 implies either a hard delivery cap or a reporting artifact. Removing artificial constraints could unlock volume for higher-CVR campaigns.
- [PROPOSED] `scale` on `Campaign 4` (confidence 0.78): CPA 33.75 is at or below target 50.00.
- [PROPOSED] `scale` on `Campaign 3` (confidence 0.78): CPA 33.57 is at or below target 50.00.
- [PROPOSED] `scale` on `Campaign 2` (confidence 0.78): CPA 33.33 is at or below target 50.00.
- [PROPOSED] `scale` on `Campaign 1` (confidence 0.78): CPA 33.00 is at or below target 50.00.
- [PROPOSED] `Set a hard CPA guardrail alert at $34.00 for Campaign 4 and review weekly; if CPA breaches threshold, pause and redistribute budget to Campaigns 1 and 2.` on `Campaign 4` (confidence 0.78): Campaign 4 already has the highest CPA at $33.75, which is closest to breaching a reasonable $34 target ceiling. Proactive monitoring prevents budget waste if performance deteriorates.
- [PROPOSED] `Increase Campaign 2 budget by 10-15% as a primary scale test given its balanced CPA ($33.33), mid-range CPC ($0.91), and stable CVR (2.73%).` on `Campaign 2` (confidence 0.75): Campaign 2 sits at the efficiency midpoint across all KPIs and represents the lowest-risk scaling candidate. Its CPM ($13.33) is below average, suggesting available inventory headroom.
- [PROPOSED] `fix_or_reduce` on `Campaign 4` (confidence 0.72): Entity is in the weakest efficiency cohort by CPA.
- [PROPOSED] `fix_or_reduce` on `Campaign 3` (confidence 0.72): Entity is in the weakest efficiency cohort by CPA.
- [PROPOSED] `fix_or_reduce` on `Campaign 2` (confidence 0.72): Entity is in the weakest efficiency cohort by CPA.
- [PROPOSED] `Reallocate 15-20% of Campaign 4 budget to Campaign 1 to reduce blended CPA while maintaining conversion volume, then monitor whether Campaign 1 CVR scales or degrades under increased spend.` on `Campaign 4 / Campaign 1` (confidence 0.72): Campaign 4 has the highest CPA ($33.75) and highest spend ($810) while Campaign 1 has the lowest CPA ($33.00) and lowest spend ($495). Shifting budget toward the more efficient campaign should reduce portfolio CPA without sacrificing conversion count.
- [PROPOSED] `scale` on `Campaign 4` (confidence 0.68): Entity is among top spend leaders with viable efficiency indicators.
- [PROPOSED] `scale` on `Campaign 3` (confidence 0.68): Entity is among top spend leaders with viable efficiency indicators.
- [PROPOSED] `scale` on `Campaign 2` (confidence 0.68): Entity is among top spend leaders with viable efficiency indicators.
