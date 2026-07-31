"""RL observation models for LuckyRobots."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


@dataclass(frozen=True)
class CameraFrame:
    """A single camera frame returned from the engine."""
    name: str
    data: bytes
    width: int
    height: int
    channels: int
    frame_number: int
    # Depth frames only: metres per uint16 code, so `metres = code * depth_scale`. 0 on colour
    # frames. Without it a gray16 depth frame is only uncalibrated integers.
    depth_scale: float = 0.0


class ObservationResponse(BaseModel):
    """RL observation data from an agent.

    This is the return type for LuckyEngineClient.step(). It contains the RL observation vector
    with optional named access for debugging.

    Usage:
        obs = client.step(actions)

        # Flat vector for RL training
        obs.observation  # [0.1, 0.2, 0.3, ...]

        # Named access (if schema was fetched). Names come from the agent's observation
        # spec, one per term rather than one per scalar, so a 12-joint "joint_pos" block
        # is a single name covering 12 entries of the flat vector above.
        obs["projected_gravity"]  # 0.1
        obs.to_dict()  # {"base_lin_vel": 0.1, "projected_gravity": 0.2, ...}
    """

    model_config = ConfigDict(frozen=True)

    observation: List[float] = Field(
        description="Flat observation vector from the agent's observation spec"
    )
    actions: List[float] = Field(description="Last applied actions")
    timestamp_ms: int = Field(description="Wall-clock timestamp in milliseconds")
    frame_number: int = Field(description="Monotonic frame counter")
    agent_name: str = Field(description="Agent identifier")

    # Optional named access (populated if schema is available)
    observation_names: Optional[List[str]] = Field(
        default=None,
        description="Observation names from agent schema (enables named access)",
    )
    action_names: Optional[List[str]] = Field(
        default=None,
        description="Action names from agent schema",
    )
    camera_frames: List[CameraFrame] = Field(
        default_factory=list,
        description="Camera frames synchronized with this observation",
    )

    # Enriched step data (populated when a negotiated task session is active)
    reward_signals: Optional[Dict[str, float]] = Field(
        default=None,
        description="Engine-computed reward signals keyed by term name (unweighted)",
    )
    terminated: bool = Field(
        default=False,
        description="True if a hard termination condition was triggered",
    )
    truncated: bool = Field(
        default=False,
        description="True if the episode was truncated (e.g., time limit)",
    )
    info: Optional[Dict[str, float]] = Field(
        default=None,
        description="Auxiliary info for diagnostics",
    )
    termination_flags: Optional[Dict[str, bool]] = Field(
        default=None,
        description="Per-condition termination flags",
    )

    def __getitem__(self, key: str) -> float:
        """Access observation value by name.

        Args:
            key: Observation name from the agent schema (e.g., "projected_gravity",
                "joint_pos"). Names are per observation term, not per scalar.

        Returns:
            The observation value.

        Raises:
            KeyError: If names not available or key not found.
        """
        if self.observation_names is None:
            raise KeyError(
                f"No observation names available. "
                f"Ensure client has fetched schema via get_agent_schema()."
            )
        try:
            idx = self.observation_names.index(key)
            return self.observation[idx]
        except ValueError:
            raise KeyError(
                f"Unknown observation name: '{key}'. "
                f"Available: {self.observation_names}"
            )

    def get(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """Get observation value by name with optional default.

        Args:
            key: Observation name.
            default: Value to return if key not found.

        Returns:
            The observation value or default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def to_dict(self) -> Dict[str, float]:
        """Convert observations to a name->value dictionary.

        Returns:
            Dict mapping observation names to values. If names not available,
            uses "obs_0", "obs_1", etc.
        """
        if self.observation_names is not None:
            return dict(zip(self.observation_names, self.observation))
        return {f"obs_{i}": v for i, v in enumerate(self.observation)}

    def actions_to_dict(self) -> Dict[str, float]:
        """Convert actions to a name->value dictionary.

        Returns:
            Dict mapping action names to values. If names not available,
            uses "action_0", "action_1", etc.
        """
        if self.action_names is not None:
            return dict(zip(self.action_names, self.actions))
        return {f"action_{i}": v for i, v in enumerate(self.actions)}
