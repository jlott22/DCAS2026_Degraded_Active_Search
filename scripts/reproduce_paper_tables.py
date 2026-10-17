"""Recompute DCAS 2026 Tables II and III from published processed CSVs."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
METHODS = {"VP": "BWVA", "DP": "ARP", "AG": "MBTA"}
LOSSES = (0, 10, 25)
PUBLISHED_COMPUTE = {
    "VP": (0.320, 0.348, 0.352),
    "DP": (0.335, 0.367, 0.429),
    "AG": (0.324, 0.325, 0.324),
}
PUBLISHED_MESSAGES = {
    "VP": (2.499, 2.759, 3.168),
    "DP": (2.269, 2.438, 4.345),
    "AG": (2.944, 2.953, 2.992),
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def summarize() -> tuple[dict, dict]:
    robot = read_csv("published_robot_metrics.csv")
    system = read_csv("published_system_metrics.csv")
    assert len(robot) == 540 and len(system) == 135
    robot_values = defaultdict(list)
    system_values = defaultdict(list)
    robot_keys = defaultdict(set)
    system_keys = defaultdict(set)
    for row in robot:
        key = (row["source_method"], int(row["loss_percent"]))
        motor = float(row["motor_time_ms"])
        compute = float(row["compute_time_ms"])
        robot_values[key].append(compute / (motor + compute))
        robot_keys[key].add((int(row["trial"]), row["robot_id"]))
    for row in system:
        key = (row["source_method"], int(row["loss_percent"]))
        system_values[key].append(float(row["msgs_sent"]) / float(row["unique_cells"]))
        system_keys[key].add(int(row["trial"]))
    compute_means = {}
    message_means = {}
    for method in METHODS:
        for loss in LOSSES:
            key = (method, loss)
            assert len(robot_keys[key]) == len(robot_values[key]) == 60, key
            assert len(system_keys[key]) == len(system_values[key]) == 15, key
            assert system_keys[key] == set(range(15)), key
            compute_means[key] = mean(robot_values[key])
            message_means[key] = mean(system_values[key])
    return compute_means, message_means


def display(title: str, values: dict, expected: dict) -> None:
    print(f"\n{title}")
    print("Method       0%      10%      25%")
    for method, paper_name in METHODS.items():
        measured = [values[(method, loss)] for loss in LOSSES]
        for actual, published in zip(measured, expected[method]):
            assert round(actual, 3) == published, (method, actual, published)
        print(f"{paper_name:<8} " + " ".join(f"{value:8.3f}" for value in measured))


if __name__ == "__main__":
    computation, messages = summarize()
    display("Table II: onboard computation fraction", computation, PUBLISHED_COMPUTE)
    display("Table III: messages per unique searched cell", messages, PUBLISHED_MESSAGES)
    print("\nAll 135 system trials and published rounded values verified.")
