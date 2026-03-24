---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- climatelag
- computational-economics
- environmental/climate-economics
- emerging-terminology
pretty_name: Climatelag Economics Dataset
size_categories:
- n<1K
---

# Climatelag Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Climatelag` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Environmental/Climate Economics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `year`: Synthetic climate-policy year
- `emission_flow`: Current greenhouse gas emission flow intensity
- `atmospheric_stock`: Accumulated atmospheric greenhouse stock pressure
- `response_delay`: Delay in climate-system response to forcing
- `damage_realization_lag`: Lag between forcing and realized economic damage
- `policy_delay`: Delay between policy adoption and effective implementation
- `discounting_bias`: Present-bias/discounting distortion against long-run damages
- `adaptation_capacity`: Capacity to adapt and mitigate delayed impacts
- `climatelag_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Climatelag applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{climatelag2026,
title={{Climatelag Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
