import click
from qplay_cli.dataset.commands import dataset
from qplay_cli.backtest.commands import backtest
from qplay_cli.user.commands import user
from qplay_cli.machine.commands import machine

@click.group()
def quantplay():
    pass

quantplay.add_command(dataset)
quantplay.add_command(backtest)
quantplay.add_command(user)
quantplay.add_command(machine)
    
if __name__ == '__main__':
    quantplay()