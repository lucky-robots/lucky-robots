# Changelog

## 0.5.0 (2026-07-30) — NIR materials: what a surface is made of

0.4.0 told you *where* things are. This release adds *what they are*. The engine's
LiDAR and depth camera now share one near-infrared material model, so glass, water,
mirrors and retroreflectors behave the way they do in front of a real 905 nm sensor —
and this release exposes that to Python.

### Added

- **Return strength** — `client.get_lidar_scan(..., want_intensity=True)` fills two
  new per-beam channels alongside `ranges`:
  - `intensity` — what the receiver actually saw, so it carries 1/R² falloff and
    saturates close in.
  - `reflectivity_calibrated` — the same return with range divided back out, in
    multiples of a perfect Lambertian at normal incidence. This is the one to compare
    across distances when you're judging what a surface is made of.

  Both need `material=True` to mean anything, and both use `-1.0` for "not
  resolvable" — the bake had no material at that hit, so the geometry is still real
  but the material is unknown.

- **Multi-return** — `client.set_lidar_secondary_capture(capture, scope)` controls what
  a beam does after its first hit: pass through it (glass → the wall behind), fold off
  it (mirror), or both. `secondary_ranges` then carries the second hit per beam.

- **Material bake control** —
  - `client.bake_lidar_material(cell_size, max_dim, splat_radius, include_hidden)`
    builds the voxel bake that maps a physics hit back to its rendered material. Every
    argument falls back to the scene's own setting, so calling it bare just rebuilds.
    `splat_radius` is worth setting: at 0 the bake fills only the cells a triangle
    crosses while the lookup is nearest-cell, which measured 27.5% of rays missing the
    bake against 1.3% at radius 1.
  - `client.get_lidar_bake_status()` reports what's baked — format, extent, occupancy —
    and, importantly, `stale`. A stale bake still answers, but it answers with the
    materials as they were when it was baked.

- **Camera configuration** — `client.get_camera_config(name)` and
  `client.set_camera_config(name, config)` expose resolution, depth recording,
  `depth_scale`, and the depth `sensor_model` (clean z-buffer, ActiveStereo, iToF,
  StructuredLight, dToFSparse) with its calibration.

  They also expose `debug_channel`, a diagnostic selector: set it non-zero and the
  camera replaces each pixel's range with an internal term of the sensor model —
  backscatter, incidence cosine, NIR reflectivity, metalness, roughness, transmission
  suppression, continuation class, or stereo occlusion reject. That stream is **not** a
  depth map, and a recording made with one set says so in its `info.json`. Set it back
  to 0 when you're done.

### Usage

```python
# Bake first — the material channels and multi-return both read the voxel bake, which is
# what maps a physics hit back to the material that was rendered there.
client.bake_lidar_material(cell_size=0.05, splat_radius=1, timeout=120.0)
st = client.get_lidar_bake_status()
assert st.valid and not st.stale          # a stale bake answers with the OLD materials

# Per-beam material strength. reflectivity_calibrated is the range-compensated one.
scan = client.get_lidar_scan(material=True, want_intensity=True)

# Multi-return needs BOTH gates: the capture mode AND a sensor modelled with >= 2 echoes.
# Single-echo hardware (Unitree L1, Livox Mid-360) cannot report a ghost, so the live path
# withholds it no matter what capture is set to.
client.set_lidar_secondary_capture(capture=3, scope=1)     # 3 = both, 1 = all surfaces
p = client.lidar.GetLidarReturnParams(client.pb.lidar.GetLidarReturnParamsRequest())
client.lidar.SetLidarReturnParams(client.pb.lidar.SetLidarReturnParamsRequest(
    max_range_at_ref=p.max_range_at_ref, ref_reflectivity=p.ref_reflectivity,
    range_exp=p.range_exp, noise_sigma0=p.noise_sigma0,
    grazing_cos_cutoff=p.grazing_cos_cutoff, intensity_ref_range=p.intensity_ref_range,
    detect_floor=p.detect_floor, near_range_r0=p.near_range_r0,
    noise_slope_per_m=p.noise_slope_per_m, max_returns=2))
scan = client.get_lidar_scan(material=True, want_secondary=True)

# Camera: read the config, change one field, put it back.
cfg = client.get_camera_config("front_camera").config
new = client.pb.camera.CameraConfig(); new.CopyFrom(cfg)
new.debug_channel = 8                     # continuation class; 0 = real depth
client.set_camera_config("front_camera", new)
```

A diagnostic channel is NOT depth — set it back to 0 when you are done reading it.

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

Runtime PD/scale tuning, soft scene reset, gRPC-driven editor play/stop, and
recording-aware metadata.

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
- Additive against the v0.2.0 engine API: every existing task-contract /
  action-group / progress RPC is preserved, as are the `LuckyEnv` and
  `reflection.py` modules.
