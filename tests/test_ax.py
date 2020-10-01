from ax import optimize


def dont_test_intro_example():
    """ https://ax.dev/ """
    best_parameters, best_values, experiment, model = optimize(
        parameters=[
            {
                "name": "x1",
                "type": "range",
                "bounds": [-10.0, 10.0],
            },
            {
                "name": "x2",
                "type": "range",
                "bounds": [-10.0, 10.0],
            },
        ],
        # Booth function
        evaluation_function=lambda p: (p["x1"] + 2 * p["x2"] - 7) ** 2 + (2 * p["x1"] + p["x2"] - 5) ** 2,
        minimize=True,
    )
    return best_values


if __name__ == '__main__':
    dont_test_intro_example()


warnign_0_1_16 = """
[INFO 09-30 20:54:49] ax.service.managed_loop: Running optimization trial 20...
/Users/petercotton/virtual-envs/tuneup/lib/python3.7/site-packages/ax/modelbridge/torch.py:311: UserWarning:

To copy construct from a tensor, it is recommended to use sourceTensor.clone().detach() or sourceTensor.clone().detach().requires_grad_(True), rather than torch.tensor(sourceTensor).
"""

error_0_1_15 = """
/Users/petercotton/virtual-envs/tuneup/bin/python3 /Users/petercotton/github/tuneup/tests/test_ax.py
Traceback (most recent call last):
  File "/Users/petercotton/github/tuneup/tests/test_ax.py", line 1, in <module>
    from ax import optimize
  File "/Users/petercotton/virtual-envs/tuneup/lib/python3.7/site-packages/ax/__init__.py", line 31, in <module>
    from ax.modelbridge import Models
  File "/Users/petercotton/virtual-envs/tuneup/lib/python3.7/site-packages/ax/modelbridge/__init__.py", line 10, in <module>
    from ax.modelbridge.factory import (
  File "/Users/petercotton/virtual-envs/tuneup/lib/python3.7/site-packages/ax/modelbridge/factory.py", line 22, in <module>
    from ax.modelbridge.registry import (
  File "/Users/petercotton/virtual-envs/tuneup/lib/python3.7/site-packages/ax/modelbridge/registry.py", line 48, in <module>
    from ax.models.torch.botorch_modular.model import BoTorchModel
ModuleNotFoundError: No module named 'ax.models.torch.botorch_modular'
"""