import numpy as np
import pytest

from spacenormal.config import load_config, load_scenarios
from spacenormal.data import synthetic
from spacenormal.sim.interface import Scenario

CREW = ["C1", "C2", "C3", "C4"]


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture(scope="session")
def scenarios():
    return {name: Scenario.from_dict(name, spec) for name, spec in load_scenarios().items()}


@pytest.fixture(scope="session")
def make(cfg, scenarios):
    def _make(name: str, seed: int = 0):
        return synthetic.make_mission(CREW, scenarios[name], np.random.default_rng(seed), cfg)
    return _make
