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

    # Create the ping command to send to the terminal - note that the repeat
    # command is different on Windows and Unix based operating systems
    OS = system().lower()
    hostname = "oldschool{}.runescape.com".format(world_number)
    if OS == "windows":
        repeat = "-n {}".format(n_tests)
    elif OS == "darwin" or OS == "linux":
        repeat = "-c {}".format(n_tests)
    ping_command = "ping {} {}".format(repeat, hostname)

    print("{}".format(ping_command))

    # Now send the ping command to the terminal and capture stdout and stderr,
    # then decode the bytes string into UTF-8 and split the list
    ping = Popen(ping_command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = ping.communicate()
    stdout_split = stdout.decode("utf-8").split()

    # Now we need to find where the average latency is output - note that this
    # is different between Windows and Unix based operating systems again
    if OS == 'windows':
        if stdout[-1] == b'loss),':
            avg_latency = 999
        else:
            avg_latency = int(''.join(findall(r'\d', str(stdout[-1]))))
    elif OS == "darwin" or OS == "linux":
        avg_ping_idx = -1
        for i in range(len(stdout_split)):
            if stdout_split[i] == "min/avg/max/stddev":
                avg_ping_idx = i + 2
                break
        if avg_ping_idx == -1:
            raise IndexError("Couldn't find average latency for {}"
                             .format(hostname))
        avg_latency = stdout_split[avg_ping_idx].replace("/", " ").split()[1]

    return avg_latency


def main():
    """
    The main control function

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    n_args = len(argv)

    if n_args >= 2:
        n_tests = 5
        world_type = argv[1].lower()
        if world_type == "uk":
            print("Pinging all of the non-PvP UK worlds")
            worlds = [2, 9, 10, 17, 18, 33, 34, 41, 42, 49, 50, 58, 65, 66, 73]
        elif world_type == "allworlds":
            print("Pinging all of the RuneScape worlds")
            worlds = range(1, 125)
        elif world_type == "custom":
            print("List the worlds wanted to be pinged separated by a space, e.g. 1 12 42")
            custom_worlds = input("Worlds: ")
            worlds = [int(i) for i in custom_worlds.split()]
        elif world_type.isdigit() is True:
            worlds = [int(argv[1])]
        else:
            raise ValueError("\n\nBAD WORLD SELECTION!\nAcceptable choices are: uk, allworlds, custom or a single world number.")
        print("Using default n_tests value: {}".format(n_tests))

    if n_args >= 3:
        n_tests = int(argv[2])

    if n_tests > 5:
        print("Pinging each world {} times, this may take a while.."
              .format(n_tests))

    print("")

    # Now iterate through each world and run the ping test
    pings = []
    for world in worlds:
        world_ping = world_avg_ping(world, n_tests)
        pings.append("World {}".format(world))
        pings.append(world_ping)

    # Now figure out which world had the lowest ping
    # The latency is index 1, 3, 5, ... etc and 0, 2, 4, .. etc is the
    # world number
    lowest_ping = min(pings[1::2])
    lowest_ping_world_number = pings[pings.index(lowest_ping) - 1]
    print('\nLowest ping:\n{} {} ms'.format(lowest_ping_world_number,
          lowest_ping))

    return None


if __name__ == '__main__':
    main()
