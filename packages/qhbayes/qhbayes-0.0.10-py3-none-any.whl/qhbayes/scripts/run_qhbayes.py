import ast

import click
import matplotlib.pyplot as plt
from numpy import atleast_1d
from qhbayes.app import make_dashboard
from qhbayes.data import IVESPA, Aubry, Mastin, Sparks
from qhbayes.notebooks import launch_jupyter_example


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


def run_app(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    make_dashboard()
    ctx.exit()


def run_example(ctx, param, value):
    """Run a QHBayes jupyter notebook example.

    n is the example number; choices are 1, 2"""

    print(param)
    print(value)

    click.echo(f"Running QHBayes Example {value}")

    launch_jupyter_example(value)


@click.command()
@click.option(
    "--app", is_flag=True, callback=run_app, expose_value=False, is_eager=True
)
@click.option(
    "--example",
    type=click.Choice(["1", "2"]),
    default="1",
    callback=run_example,
    expose_value=True,
    is_eager=True,
)
@click.option(
    "-data",
    "--dataset",
    type=click.Choice(["Mastin", "Sparks", "Aubry", "IVESPA"], case_sensitive=False),
    prompt="Select dataset",
    required=True,
)
@click.option(
    "-x",
    "--xvar",
    type=click.Choice(["H", "Q", "MER"], case_sensitive=False),
    prompt="Set explanatory variable",
    help="Set explanatory variable",
    required=True,
)
@click.option(
    "-obs",
    "--observation",
    cls=PythonLiteralOption,
    default='"10.0"',
    prompt="Set observations (e.g. '[10., 15.]'",
    help="Set observation",
    required=True,
)
@click.option(
    "-s",
    "--samples",
    type=int,
    default=1000,
    prompt="Set number of samples to draw from the posterior predictive distribution",
    help="Number of samples to draw from the posterior predictive distribution",
)
def run_qhbayes(dataset: str, xvar: str, observation: float, samples: int) -> None:
    print("Running QHBayes")
    if xvar == "H":
        yvar = "Q"
    else:
        yvar = "H"
    print(f"{dataset} {yvar}|{xvar}")

    if dataset == "Mastin":
        data = Mastin
    elif dataset == "Sparks":
        data = Sparks
    elif dataset == "Aubry":
        data = Aubry
    else:  # args.dataset == 'IVESPA':
        data = IVESPA

    data.set_vars(xvar=xvar, yvar=yvar)  # sets independent and variables

    data.mle(plot=True)  # maximum likelihood estimator (Mastin curve)

    data.posterior_plot()  # Now plot the curve.

    print(observation)
    observation = [float(obs) for obs in observation]
    observation = atleast_1d(observation)
    print(observation)

    data.set_obs(observation)  # Example -- set observed H to 10 km

    data.posterior_simulate(
        samples, plot=True, split_x=(True if len(observation) > 1 else False)
    )  # Sample from the posterior distribution (get MER values) for 1000 samples, and plot it

    plt.show()
