# Decentralized task allocation in Bayesian search under degraded communications

Paper release for **“Decentralized Task-Allocation in Bayesian Search: An Empirical Study Under Degraded Communications”** by James Lott and Vahraz Honary (DCAS 2026). This repository contains the three four-robot implementations, the saved 19 × 19 paired scenarios, processed measurements for all 135 published trials, and a script that recomputes the paper's computation and messaging tables.

## Reproduce the published tables

Python 3.10 or newer is sufficient for the processed-data check; no robot hardware or third-party Python package is needed.

```bash
python scripts/reproduce_paper_tables.py
```

The script checks 15 paired scenarios × 3 methods × 3 receiver-side loss conditions. It prints Table II (onboard computation fraction) and Table III (messages per unique searched cell) and verifies their published rounded values. The included CSVs are processed exports from the experiment workbook; the original workbook and raw logs are retained in the separate research archive.

## Repository map

| Path | Purpose |
| --- | --- |
| `hardware/robots/` | Experiment snapshots for belief-weighted Voronoi allocation (`Voronoi-partitioning.py`), adaptive rectangular partitioning (`Dynamic-Partitioning.py`), and market-based assignment (`Auction-Greedy.py`). |
| `hardware/bridge/` | ESP32 MQTT-to-UART bridge used with the robots. |
| `hardware/hub/` | MQTT metrics collector. |
| `scenarios/` | Scenario generator retained with the experiment. |
| `data/published_scenarios.csv` | The 15 saved paired target/clue layouts used in the published comparison. |
| `data/published_robot_metrics.csv` | 540 processed robot records, four robots per trial. |
| `data/published_system_metrics.csv` | 135 processed system trial records. |
| `scripts/reproduce_paper_tables.py` | Standard-library table regeneration and structural checks. |
| `DATA_DICTIONARY.md` | Fields, units, methods, and averaging rules. |

## Hardware use

The robot programs target Pololu 3pi+ 2040 robots running MicroPython with the `pololu_3pi_2040_robot` library. Deploy one selected method to each of four robots. Set `ROBOT_ID` to `00`, `01`, `02`, or `03` for each device and set `msg_drop_rate` to `0.0`, `0.10`, or `0.25` for the intended condition. The archived files retain the final local settings in which they were saved. Set the MQTT broker address in `hardware/hub/metrics_hub.py` and the ESP32 sketch for your network. The hub requires `paho-mqtt`; the ESP32 sketch requires its Arduino MQTT dependencies. The saved scenario CSV fixes target and clue placements for the published comparisons.

The processed-data script is the supported no-hardware reproduction path. Hardware execution depends on the specified Pololu, ESP32, MQTT, and grid setup.

## Provenance and citation

The code and processed measurements came from the author's DCAS experiment archive, rather than the older code previously at this repository's root. `SOURCE_PROVENANCE.md` records that transition. Cite the paper using `CITATION.cff`. Author-owned code and data in this release are MIT licensed; hardware and third-party libraries retain their own licenses and are not vendored here.
