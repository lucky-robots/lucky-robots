# Changelog

## 0.4.0 (2026-07-21) — LiDAR support + camera depth (RGBD)

The headline of this release is **first-class LiDAR support**. You can now turn a
scene's LiDAR sensors on, read full range scans back over gRPC, and size your
buffers ahead of time — all without setting up a recording. Alongside it, cameras
can stream live **metric depth**, so a single camera gives you both color and
per-pixel distance (RGBD).

Everything here is wire-compatible with the engine you're already running — there's
nothing to upgrade on the engine side to start using it.

### Added

- **LiDAR API** — a new `client.lidar` service, with friendly wrappers:
  - `client.set_lidar_live(live=True)` — start (or stop) firing the LiDAR every
    step, so you can read scans even when you aren't recording. The setting sticks
    across resets, so you only need to call it once.
  - `client.get_lidar_scan(sensor=0, material=False, want_secondary=False)` — read a
    scan for a sensor (0-based). You get back `beams` (channels × azimuth bins),
    `ranges` in metres (`-1.0` means "no return"), and `secondary_ranges` when you
    ask for them.
  - `client.get_lidar_beam_count(sensor=0)` — how many beams a sensor produces
    (channels × azimuth bins); handy for pre-allocating arrays.
- **Camera depth (RGBD)** — `configure_cameras([...])` now accepts `kind="color"`
  (the default) or `kind="depth"`, plus a `format` (`"raw"`, or `"jpeg"` for color).
  Depth frames are packed as `gray16le`; turn a pixel into metres with
  `metres = code * depth_scale`, where `depth_scale` comes back on each frame.

### Usage

```python
# LiDAR — read a live scan between episodes
client.set_lidar_live(True)          # fire the sensor every step
n = client.get_lidar_beam_count()    # size your buffers up front
scan = client.get_lidar_scan()       # scan.ranges are metres, -1.0 = no return

# Camera depth — ask a camera for metric depth instead of color
client.configure_cameras([{"name": "front_cam", "kind": "depth"}])
```

Call the LiDAR reads while the simulation is idle — like the other scene-inspection
calls (`list_cameras`, `get_full_state`, …), not from inside an active `step()` loop.

## 0.3.0 (2026-05-05) — Runtime gain override, scene reset, editor play/stop

Tracks the LuckyEngine `mick/policy-fixes` branch — runtime PD/scale tuning,
soft scene reset, gRPC-driven editor play/stop, and recording-aware metadata.

### Added
- `RobotController.set_policy_gains(slot, overrides)` /
  `clear_policy_gains(slot)` for per-joint runtime PD/effort/scale/default
  override on an active slot — no descriptor reload, no policy reseed.
  Unset fields preserve descriptor values (sentinel = `None` in Python,
  `NaN` on the wire). Both sync and async (`async_robots.py`) variants.
- `Session.enter_play_mode()` / `exit_play_mode()` and `AsyncSession`
  equivalents drive the editor Edit ↔ Play state machine over gRPC.
  Async transitions; poll readiness via `get_agent_schema` /
  `get_model_info`. Session boundaries, **not** pause/resume — Exit
  tears down the active recording.
- `Session.reset_scene(preserve_time=False)` and
  `MujocoScene.reset(preserve_time=False)` — soft reset back to
  `keyframe[0]` / `qpos0`, zero ctrl/forces, reseed active PolicyRuntime
  PD targets. Recording continues across the reset.
- New proto messages — `JointGainOverride`, `EnterPlayMode{Request,
  Response}`, `ExitPlayMode{Request,Response}`, `ResetScene{Request,
  Response}` — and five new RPCs (`SetPolicyGains`, `ClearPolicyGains`,
  `EnterPlayMode`, `ExitPlayMode`, `ResetScene`).

### Notes
- The recording Parquet schema gained a new `frame_flags : uint8` column
  (set engine-side). Bit 0 = `new_policy_step` (this substep ran fresh
  ONNX inference vs. holding the previous action under decimation),
  bit 1 = `post_reset` (first frame after `ResetScene`). Existing
  consumers ignore the column; new consumers should filter on it for
  correct IL training under decimation.
- Generated `*_pb2.py` / `*_pb2_grpc.py` regenerated with
  `grpcio-tools` 1.80.0 (was 1.78.0 in 0.2.0). The only functional
  difference in untouched-service stubs is the version-string constant.

## 0.2.0 (2026-04-27) — Policy + MujocoScene API

Substantial expansion to support LuckyEngine's `policy-redo` branch
(multi-slot PolicySlot, MotionGraph gating, runtime descriptor swap) and the
upgraded MujocoSceneService.

### Added
- `RobotController` high-level wrapper covering all 21 new policy + motion-
  graph RPCs (slot activation, descriptor swap, driven-joints mask, command
  store, motion-graph inputs, base pose, last action, streaming state).
- `MujocoScene` high-level wrapper for the upgraded MujocoSceneService:
  ownership map on `GetModelInfo`, `StateFilter`-aware streaming, policy-
  claim-aware `SetControl`, fully-implemented `SetQpos` with automatic PD
  reseed, `GetActuatorGains` for `NeutralizeActuatorsForTorquePolicy`
  diagnostics.
- `set_robot_pose` helper (qpos-layout-aware teleport).
- `validate_session` startup-validation pass with structured warnings.
- `validate_session` and reflection-based `has_rpc` for runtime feature
  detection (lets clients gracefully degrade against older engines).
- 4 new example scripts: single_policy_with_commands, policy_descriptor_hot_swap,
  scene_introspection, actuator_gain_inspector.
- Type stubs (`py.typed` marker) for IDE autocomplete.
- `luckyrobots inspect <host:port>` CLI for one-shot diagnostics.

### Changed
- `RobotController.get_last_action` now returns `(np.ndarray, list[str])`
  instead of `(list, list)` for direct numpy interop.

### Notes
- Generated stubs use absolute imports (matching upstream convention).
- Vendored against engine `mick/policy-redo` branch which integrates and
  extends `mick/grpc-api` (the original v0.2.0 base): preserves all
  existing task-contract / action-group / progress RPCs and
  `LuckyEnv` / `reflection.py` modules.
