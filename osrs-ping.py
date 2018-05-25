from sys import argv
from re import findall
from platform import system
from subprocess import Popen, PIPE


def osrs_avg_ping(world_number, n_tests=5):
    """
    Returns the average latency of an OldSchool RuneScape server.

    Parameters
    ----------
    world_number: int.
        The world number for which the latency will be measured.
    n_tests: int.
        The number of times to ping the OldSchool RuneScape server.

    Returns
    -------
    avg_latency: int.
        The average latency for the OldSchool RuneScape server being tested,
        measured in milliseconds.
    """

    assert(type(world_number) == int)
    assert(type(n_tests) == int)

    # create a ping command
    host = 'oldschool' + str(world_number) + '.runescape.com'
    ping_param = '-n {} '.format(n_tests) if system().lower() == 'windows' \
        else '-c {} '.format(n_tests)
    ping_command = 'ping ' + ping_param + host

    ping = Popen(ping_command, stdout=PIPE, shell=True)
    output = ping.communicate()[0].split()

    if system().lower == 'windows':
        if output[-1] == b'loss),':
            avg_latency = 999
        else:
            avg_latency = int(''.join(findall(r'\d', str(output[-1]))))
    else:
        print(output[-2])
        avg_latency = 999

    return avg_latency


if __name__ == '__main__':

    n_args = len(argv)

    if argv[1] == 'uk':
        print('Pinging all non-PvP UK worlds.')
        worlds = [2, 9, 10, 17, 18, 33, 34, 41, 42, 49, 50, 58, 65, 66, 73]
    elif argv[1] == 'allworlds':
        print('Pinging all the worlds.')
        worlds = range(1, 95)
    elif argv[1] == 'custom':
        print('List the worlds separated by a space, e.g. 1 12 42')
        custom_worlds = input('Worlds: ')
        worlds = [int(i) for i in custom_worlds.split()]
    else:
        print('Bad world section. Exciting script.')
        print('Acceptable worlds are: uk, allworlds and custom.')
        raise ValueError()

    if n_args == 2:
        print('Number of ping tests not provided. Using default value: 1.')
        n_tests = 1
    else:
        n_tests = int(argv[2])

    pings = []
    for world in worlds:
        world_ping = osrs_avg_ping(world, n_tests)
        pings.append("World {}".format(world))
        pings.append(world_ping)

    # the latency is index 1, 3, 5, ... etc
    lowest_ping = min(pings[1::2])
    lowest_ping_world = pings[pings.index(lowest_ping) - 1]

    print('\nLowest ping:\n{}, ping = {} ms'.format(
            lowest_ping_world, lowest_ping))
