#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""

print("Loading the reporter...")

def by_count_then_name(pair):
    count, name = pair
    return (-count, name)

def get_user(log_line):
    return log_line.split()[1]

def get_time_stamp(log_line):
    return log_line.split()[0][11:13]

def get_action(log_line):
    return log_line.split()[2]

def count_and_rank(log_lines, get_key):
    count_list = {}
    for log_line in log_lines:
        key = get_key(log_line)
        count_list[key] = count_list.get(key, 0) + 1

    pair_list = [(count, key) for key, count in count_list.items()]
    pair_list.sort(key=by_count_then_name)
    return pair_list

def main():
    with open("cloudbyte_access.log", "r") as log_file:
        log_lines = [line for line in log_file ]

    first_ts = log_lines[0].split()[0]
    last_ts = log_lines[-1].split()[0]
    first = f"{first_ts[:10]} {first_ts[11:]}"
    last = f"{last_ts[:10]} {last_ts[11:]}"

    print("Cloud Access Report")
    print(f"{len(log_lines)} events from {first} to {last}")
    print()

    for log_line in log_lines:
        log_elements = log_line.split()
        date = log_elements[0][:10]
        time = log_elements[0][11:]
        print(f"{date} {time} {log_elements[1]} {log_elements[2]}")

    print()

    #Most active Users
    user_pairs = count_and_rank(log_lines, get_user)
    print("Most active users:")
    for rank, (count, username) in enumerate(user_pairs, start=1):
        print(f"{rank}. {username}: {count} events")

    print()

    #Busiest hours
    hour_pairs = count_and_rank(log_lines, get_time_stamp)
    print("Most active hours:")
    for count, hours in hour_pairs:
        print(f"{hours}:00 {count} events")

    print()

    #Activity by type.
    action_pairs = count_and_rank(log_lines, get_action)
    print("Activity by type")
    for rank, (count, action) in enumerate(action_pairs, start=1):
        print(f"{rank}. {action}: {count} events")

    print()

    #Most active logins
    logins = [login for login in log_lines if get_action(login) == "login"]
    login_pairs = count_and_rank(logins, get_user)
    print("Most active logins:")
    for rank, (count, username) in enumerate(login_pairs, start=1):
        print(f"{rank}. {username}: {count} events")

    print()

    #Activity for one user
    person = "alice"
    persons_login = [persons for persons in log_lines if get_user(persons) == person]
    persons_login_pairs = count_and_rank(persons_login, get_action)
    print(f"Activity by {person}:")
    for rank, (count, action) in enumerate(persons_login_pairs, start=1):
        print(f"{rank}. {action}: {count} events")


if __name__ == "__main__":
    main()
