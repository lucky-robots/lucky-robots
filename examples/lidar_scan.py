"""
Read a single LiDAR scan from LuckyEngine over gRPC.

A tiny, friendly tour of the LiDAR surface: this connects to an
already-running LuckyEngine, switches the LiDAR into live mode so it keeps
firing even when you're not recording, grabs one scan from the first sensor,
and prints a short summary — how many beams the sensor has, how many of them
actually hit something, and the nearest / average / farthest hit distance in
metres. A beam that saw nothing reports a range of -1.0, and those "no return"
beams are left out of the distance stats.

Run:
    uv run python examples/lidar_scan.py
"""

from __future__ import annotations

from luckyrobots import Session


def main() -> None:
    with Session() as sess:
        # Attach to an already-running editor instance. (If you want this
        # script to also launch the engine, call sess.start(...) instead.)
        sess.connect(timeout_s=30.0)

        client = sess.engine_client

        # Wake the LiDAR so it fires every step, not just while recording.
        # You only need to ask once — it stays on across resets.
        client.set_lidar_live(True)

        # Grab one scan from the first LiDAR sensor (sensor index 0). These
        # scene-inspection calls happen while the simulation is resting quietly
        # between episodes, so it's a calm moment to peek at a sensor.
        scan = client.get_lidar_scan(sensor=0)

        ranges = list(scan.ranges)
        # A range of -1.0 means that beam saw nothing, so keep only real hits.
        hits = [r for r in ranges if r >= 0.0]

        print(f"[lidar] sensor 0 has {scan.beams} beams")
        print(f"[lidar] {len(hits)} of {len(ranges)} beams returned a hit")

        if hits:
            nearest = min(hits)
            farthest = max(hits)
            average = sum(hits) / len(hits)
            print(
                f"[lidar] hit range  "
                f"min={nearest:.3f} m  mean={average:.3f} m  max={farthest:.3f} m"
            )
        else:
            print("[lidar] no beams returned a hit this scan")


if __name__ == "__main__":
    main()
