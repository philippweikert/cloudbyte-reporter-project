#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""

print("Loading the reporter...")

def main():

    log_lines = []
    with open("cloudbyte_access.log" , "r") as log_file:
        for line in log_file:
            log_lines.append(line)

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

    #Actions counted by each user
    user_counts = {}
    for log_line in log_lines:
        username = log_line.split()[1]
        user_counts[username] = user_counts.get(username, 0) + 1

    #print(user_counts)

    #Counting and sorting the users by actions
    user_pairs = []
    for username, count in user_counts.items():
        user_pairs.append((count, username))

    user_pairs.sort(reverse=True)

    #Most active Users
    for rank, (count, username) in enumerate(user_pairs, start=1):
        print(f"{rank}. {username}: {count} events")

if __name__ == "__main__":
    main()
