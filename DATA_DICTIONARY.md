# Data dictionary

## Conditions

`source_method` identifies the saved program (`VP`, `DP`, `AG`). The paper names are `BWVA` (belief-weighted Voronoi allocation), `ARP` (adaptive rectangular partitioning), and `MBTA` (market-based task assignment), respectively. `loss_percent` is receiver-side simulated message loss: 0, 10, or 25. Each method/loss pair has 15 trial IDs, numbered 0–14, and four robot records per trial. Scenario CSV episode 1 corresponds to trial ID 0.

## `data/published_robot_metrics.csv`

`robot_id` is a two-digit device identifier. `steps` is the robot's movement count. `msgs_sent` and `msgs_received` are MQTT message counts. `motor_time_ms`, `compute_time_ms`, and `busy_ms` are millisecond counters from the metrics hub. The paper's Table II uses the mean, over the 60 robot records in each condition, of `compute_time_ms / (motor_time_ms + compute_time_ms)`.

## `data/published_system_metrics.csv`

One record represents a four-robot system trial. `system_steps` is summed robot movement. `unique_cells` is the system's unique searched-cell count; `revisits` is the recorded repeat-visit count; `msgs_sent` is the system message count. The paper's Table III averages `msgs_sent / unique_cells` over 15 trials within each condition. Ratios are calculated per record before averaging.

## `data/published_scenarios.csv`

`object_x`, `object_y` are target coordinates. Four `clueN_x`, `clueN_y` pairs are clue coordinates. Coordinates are zero based on a 19 × 19 grid. These are the first 15 saved scenarios from the experiment's scenario file; no replacement seed or layout was generated for this release.
