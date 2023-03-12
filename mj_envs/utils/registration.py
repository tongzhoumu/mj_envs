import re

import gym

REGISTERED_ENV_IDS = set()
env_id_re = re.compile(r"^(?:[\w:-]+\/)?([\w:.-]+)-v(\d+)$")


def register(name, entry_point, max_episode_steps, kwargs):
    """A wrapper of gym.register."""
    if name in REGISTERED_ENV_IDS:
        gym.logger.warn(f"{name} is registered in gym already!")
    else:
        REGISTERED_ENV_IDS.add(name)
        gym.register(
            name,
            entry_point=entry_point,
            max_episode_steps=max_episode_steps,
            kwargs=kwargs,
        )


def register_gym_env(name: str, max_episode_steps=None, **kwargs):
    """A decorator to register ManiSkill environments in gym.

    Args:
        name (str): a unique id to register in gym.

    Notes:
        `gym.EnvSpec` uses kwargs instead of **kwargs!
    """

    def _register_gym_env(cls):
        entry_point = "{}:{}".format(cls.__module__, cls.__name__)

        register(
            name,
            entry_point=entry_point,
            max_episode_steps=max_episode_steps,
            kwargs=kwargs,
        )

        return cls

    return _register_gym_env