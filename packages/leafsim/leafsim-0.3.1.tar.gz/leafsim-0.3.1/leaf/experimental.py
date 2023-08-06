import logging
import pandas as pd
from typing import Optional, List

import simpy

from power import PowerAware, PowerMeasurement

logger = logging.getLogger(__name__)


class PowerProfile:
    def __init__(self, data: pd.DataFrame, resolution: int = 1):
        # TODO sanity check or inference
        self.data = data
        self.resolution = resolution


class Battery:
    """(Way too) simple battery."""

    def __init__(self, capacity, charge_level=0):
        self.capacity = capacity
        self.charge_level = charge_level

    def update(self, energy):
        """Can be called during simulation to feed or draw energy.

        If `energy` is positive the battery is charged.
        If `energy` is negative the battery is discharged.

        Returns the excess energy after the update:
        - Positive if battery is fully charged
        - Negative if battery is empty
        - else 0
        """
        self.charge_level += energy
        excess_energy = 0

        if self.charge_level < 0:
            excess_energy = self.charge_level
            self.charge_level = 0
        elif self.charge_level > self.capacity:
            excess_energy = self.charge_level - self.capacity
            self.charge_level = self.capacity

        return excess_energy


class PowerGenerator:
    # TODO Take care that carging always smaller than max carging speed of energy_storage
    def __init__(self, env: simpy.Environment, profile: PowerProfile, energy_storage: EnergyStorage):
        self.env = env
        self.energy_storage = energy_storage
        self.process = env.process(self._generate_power(profile))

    def _generate_power(self, profile: PowerProfile):
        for t, watt in profile.data.itertuples():
            yield self.env.timeout(t + 0.01 - self.env.now)  # TODO comes last!
            self.energy_storage.charge(watt / 60 * profile.resolution)


class EmptyEnergyStorageException(Exception):
    pass

