from sys import argv
from re import findall
from platform import system
from subprocess import Popen, PIPE


def world_avg_ping(world_number, n_tests=5):
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

    assert(type(world_number) == int), "World type not an integer."
    assert(type(n_tests) == int), "Number of tests not an integer."
    assert(n_tests > 1), "The number of tests has to be greater than one."

    # Create the ping command to send to the terminal - note that the repeat command is different on Windows and Unix
    # based operating systems
    hostname = "oldschool{}.runescape.com".format(world_number)
    if system().lower == "windows":
      repeat = "-n {}".format(n_tests)
    else:
      repeat = "-c {}".format(n_tests)
    ping_command = "ping {} {}".format(repeat, hostname)

    print("Pinging: {} {}".format(repeat, hostname))

    # Now send the ping command to the terminal and capture stdout and stderr, then decode the bytes string into UTF-8
    # and split the list
    ping = Popen(ping_command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = ping.communicate()
    stdout_split = stdout.decode("utf-8").split()

    # Now we need to find where the average latency is output - note that this is different between Windows and Unix
    # based operating systems again
    if system().lower == 'windows':
        if stdout[-1] == b'loss),':
            avg_latency = 999
        else:
            avg_latency = int(''.join(findall(r'\d', str(stdout[-1]))))
    else:
        avg_ping_idx = -1
        for i in range(len(stdout_split)):
            if stdout_split[i] == "min/avg/max/stddev":  # When we find this, the time is 2 entries next
                avg_ping_idx = i + 2
                break
        if avg_ping_idx == -1:
            raise IndexError("Couldn't find average latency for {}".format(hostname))
        avg_latency = stdout_split[avg_ping_idx].replace("/", " ").split()[1]

    return avg_latency


def main():
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
        n_tests = 5
        print('Number of ping tests not provided. Using default value: {}.'.format(n_tests))
    else:
        n_tests = int(argv[2])

    if (n_tests > 5):
        print ("Pinging each world {} times, this may take a while.".format(n_tests))
    pings = []
    for world in worlds:
        world_ping = world_avg_ping(world, n_tests)
        pings.append("World {}".format(world))
        pings.append(world_ping)

    # The latency is index 1, 3, 5, ... etc and 0, 2, 4, .. etc is the world number
    lowest_ping = min(pings[1::2])
    lowest_ping_world_number = pings[pings.index(lowest_ping) - 1]
    print('\nLowest ping:\n{} {} ms'.format(lowest_ping_world_number, lowest_ping))

    return

if __name__ == '__main__':
    main()
