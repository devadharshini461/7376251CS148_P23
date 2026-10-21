# ------------------------------------------------------------
# Name          : Devadharshini S
# Register No   : 7376251IT148
# Project       : P23 - Hostel Room Allocation
# Description   : Terminal program for a hostel warden. It adds
#                 rooms, allots beds to students, vacates and
#                 transfers students, and shows vacancy and
#                 occupancy reports. Data is kept in .txt files.
# ------------------------------------------------------------

# file names
ROOMS_FILE = "rooms.txt"
ALLOT_FILE = "allotment.txt"
WAIT_FILE = "waiting.txt"

# room types and the most beds a room of that type can have
TYPE_LIST = ["Single", "Double", "Triple"]
TYPE_BEDS = {"Single": 1, "Double": 2, "Triple": 3}

# years of study, first year comes first (used for the waiting list)
YEAR_LIST = ["I", "II", "III", "IV"]

MAX_FLOOR = 10


# ------------------------------------------------------------
# reading input safely
# ------------------------------------------------------------

def read_text(prompt):
    # keep asking until the user types something and it has no | in it
    while True:
        text = input(prompt).strip()
        if text == "":
            print("  Input cannot be empty. Please try again.")
        elif "|" in text:
            print("  The | character is not allowed. Please try again.")
        else:
            return text


def read_int(prompt, low, high):
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if number < low or number > high:
            print(f"  The number must be between {low} and {high}.")
            continue
        return number


def read_name(prompt):
    # names can have letters, spaces and dots only (like "Vishal R")
    while True:
        name = read_text(prompt)
        good = True
        for ch in name:
            if not (ch.isalpha() or ch == " " or ch == "."):
                good = False
        if good:
            return name
        print("  Name can have only letters, spaces and dots.")


def read_reg(prompt):
    while True:
        reg = read_text(prompt).upper()
        if reg.isalnum():
            return reg
        print("  Register number can have only letters and digits.")


def read_year(prompt):
    while True:
        text = input(prompt).strip().upper()
        if text in YEAR_LIST:
            return text
        if text in ["1", "2", "3", "4"]:
            return YEAR_LIST[int(text) - 1]
        print("  Year must be I, II, III or IV (or 1 to 4).")


def read_block(prompt, allow_blank):
    # a block is a name made of letters, like A or B
    while True:
        text = input(prompt).strip().upper()
        if text == "" and allow_blank:
            return ""
        if text.isalpha():
            return text
        print("  Block must be letters only, for example A.")


def read_type(prompt, allow_blank):
    while True:
        text = input(prompt).strip().lower()
        if text == "" and allow_blank:
            return ""
        for name in TYPE_LIST:
            if text == name.lower():
                return name
        print("  Type must be Single, Double or Triple.")


def read_yes_no(prompt):
    while True:
        text = input(prompt).strip().lower()
        if text == "y" or text == "yes":
            return True
        if text == "n" or text == "no":
            return False
        print("  Please type y or n.")


# ------------------------------------------------------------
# loading and saving the text files
# ------------------------------------------------------------

def load_rooms():
    rooms = []
    try:
        with open(ROOMS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 5:
                    continue
                if not parts[2].isdigit() or not parts[4].isdigit():
                    continue
                if parts[3] not in TYPE_LIST:
                    continue
                room = {"no": parts[0], "block": parts[1],
                        "floor": int(parts[2]), "type": parts[3],
                        "cap": int(parts[4])}
                rooms.append(room)
    except FileNotFoundError:
        pass    # first run, no file yet
    return rooms


def load_allotments():
    allotments = []
    seen = []
    try:
        with open(ALLOT_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 4:
                    continue
                if parts[1] in seen:
                    continue    # same student twice, keep only the first
                seen.append(parts[1])
                record = {"room": parts[0], "reg": parts[1],
                          "name": parts[2], "year": parts[3]}
                allotments.append(record)
    except FileNotFoundError:
        pass
    return allotments


def load_waiting():
    waiting = []
    try:
        with open(WAIT_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 5:
                    continue
                if parts[2] not in YEAR_LIST:
                    continue
                person = {"reg": parts[0], "name": parts[1],
                          "year": parts[2], "block": parts[3],
                          "type": parts[4]}
                waiting.append(person)
    except FileNotFoundError:
        pass
    return waiting


def save_rooms(rooms):
    try:
        with open(ROOMS_FILE, "w") as f:
            for r in rooms:
                f.write(f"{r['no']}|{r['block']}|{r['floor']}|{r['type']}|{r['cap']}\n")
    except OSError:
        print("  Warning: could not save rooms.txt")


def save_allotments(allotments):
    try:
        with open(ALLOT_FILE, "w") as f:
            for a in allotments:
                f.write(f"{a['room']}|{a['reg']}|{a['name']}|{a['year']}\n")
    except OSError:
        print("  Warning: could not save allotment.txt")


def save_waiting(waiting):
    try:
        with open(WAIT_FILE, "w") as f:
            for p in waiting:
                f.write(f"{p['reg']}|{p['name']}|{p['year']}|{p['block']}|{p['type']}\n")
    except OSError:
        print("  Warning: could not save waiting.txt")


# ------------------------------------------------------------
# small helper functions
# ------------------------------------------------------------

def find_room(rooms, room_no):
    for room in rooms:
        if room["no"] == room_no:
            return room
    return None


def find_allotment(allotments, reg):
    for record in allotments:
        if record["reg"] == reg:
            return record
    return None


def find_waiting(waiting, reg):
    for person in waiting:
        if person["reg"] == reg:
            return person
    return None


def count_in_room(allotments, room_no):
    count = 0
    for record in allotments:
        if record["room"] == room_no:
            count += 1
    return count


def free_beds(room, allotments):
    free = room["cap"] - count_in_room(allotments, room["no"])
    if free < 0:
        free = 0
    return free


def year_rank(person):
    # I gives 0, II gives 1 ... so first years sort first
    return YEAR_LIST.index(person["year"])


def pick_room(rooms, allotments, block, rtype):
    # Try the best match first and then relax the preference step by step:
    # 1) block and type  2) block only  3) type only  4) any room
    steps = [(block, rtype), (block, ""), ("", rtype), ("", "")]
    for want_block, want_type in steps:
        for room in rooms:
            if want_block != "" and room["block"] != want_block:
                continue
            if want_type != "" and room["type"] != want_type:
                continue
            if free_beds(room, allotments) > 0:
                return room
    return None


def describe_match(room, block, rtype):
    block_ok = (block == "" or room["block"] == block)
    type_ok = (rtype == "" or room["type"] == rtype)
    if block_ok and type_ok:
        return "Preference matched."
    if block_ok:
        return "Preferred block given, but no free bed of the preferred type."
    if type_ok:
        return "Preferred type given, but no free bed in the preferred block."
    return "Preferred block and type are full, so the nearest free bed was used."


def get_blocks(rooms):
    blocks = []
    for room in rooms:
        if room["block"] not in blocks:
            blocks.append(room["block"])
    return sorted(blocks)


def add_to_allotments(allotments, room_no, reg, name, year):
    record = {"room": room_no, "reg": reg, "name": name, "year": year}
    allotments.append(record)
    save_allotments(allotments)


def try_waiting_list(rooms, allotments, waiting):
    # called whenever a bed becomes free (vacate, transfer, new room)
    if len(waiting) == 0:
        return
    changed = False
    # sorted keeps the arrival order for students of the same year
    order = sorted(waiting, key=year_rank)
    for person in order:
        room = pick_room(rooms, allotments, person["block"], person["type"])
        if room is None:
            break    # no bed left for anybody
        allotments.append({"room": room["no"], "reg": person["reg"],
                           "name": person["name"], "year": person["year"]})
        waiting.remove(person)
        changed = True
        print(f"  Waiting list: {person['name']} ({person['reg']}, {person['year']} year) "
              f"is now allotted room {room['no']}.")
    if changed:
        save_allotments(allotments)
        save_waiting(waiting)


# ------------------------------------------------------------
# menu options
# ------------------------------------------------------------

def add_room(rooms, allotments, waiting):
    print("\n--- Add a room ---")
    room_no = read_text("Room number (example A-204): ").upper()
    if " " in room_no:
        print("  Room number cannot have spaces.")
        return
    if find_room(rooms, room_no) is not None:
        print("  That room number already exists.")
        return
    block = read_block("Block (example A): ", False)
    floor = read_int(f"Floor (0 to {MAX_FLOOR}): ", 0, MAX_FLOOR)
    rtype = read_type("Type (Single / Double / Triple): ", False)
    most = TYPE_BEDS[rtype]
    cap = read_int(f"Capacity (1 to {most}): ", 1, most)
    rooms.append({"no": room_no, "block": block, "floor": floor,
                  "type": rtype, "cap": cap})
    save_rooms(rooms)
    print(f"  Room {room_no} added in Block {block}, floor {floor} ({rtype}, {cap} beds).")
    try_waiting_list(rooms, allotments, waiting)


def allot_student(rooms, allotments, waiting):
    print("\n--- Allot a student ---")
    if len(rooms) == 0:
        print("  There are no rooms yet. Add a room first.")
        return
    reg = read_reg("Register number: ")
    old = find_allotment(allotments, reg)
    if old is not None:
        print(f"  {old['name']} already has a bed in room {old['room']}. One student cannot get two rooms.")
        return
    if find_waiting(waiting, reg) is not None:
        print("  This student is already on the waiting list.")
        return
    name = read_name("Student name: ")
    year = read_year("Year (I / II / III / IV): ")
    block = read_block("Preferred block (press Enter for any): ", True)
    rtype = read_type("Preferred type (press Enter for any): ", True)
    room = pick_room(rooms, allotments, block, rtype)
    if room is None:
        print("  No free bed in any room right now.")
        if read_yes_no("  Add the student to the waiting list? (y/n): "):
            waiting.append({"reg": reg, "name": name, "year": year,
                            "block": block, "type": rtype})
            save_waiting(waiting)
            print(f"  {name} added to the waiting list (position {len(waiting)}).")
        return
    add_to_allotments(allotments, room["no"], reg, name, year)
    print(f"  {name} allotted to room {room['no']} (Block {room['block']}, "
          f"floor {room['floor']}, {room['type']}).")
    print("  " + describe_match(room, block, rtype))


def vacate_student(rooms, allotments, waiting):
    print("\n--- Vacate a student ---")
    reg = read_reg("Register number: ")
    record = find_allotment(allotments, reg)
    if record is None:
        print("  This student is not allotted to any room.")
        return
    print(f"  {record['name']} is in room {record['room']}.")
    if not read_yes_no("  Vacate this student? (y/n): "):
        print("  Cancelled. Nothing changed.")
        return
    allotments.remove(record)
    save_allotments(allotments)
    print(f"  {record['name']} has vacated room {record['room']}.")
    try_waiting_list(rooms, allotments, waiting)


def show_free_rooms(rooms, allotments, skip_room):
    # prints the rooms that still have a free bed, returns how many
    count = 0
    for room in rooms:
        free = free_beds(room, allotments)
        if room["no"] == skip_room or free == 0:
            continue
        print(f"    {room['no']}  Block {room['block']}  Floor {room['floor']}  "
              f"{room['type']}  free beds: {free}")
        count += 1
    return count


def transfer_student(rooms, allotments, waiting):
    print("\n--- Transfer a student ---")
    reg = read_reg("Register number: ")
    record = find_allotment(allotments, reg)
    if record is None:
        print("  This student is not allotted to any room.")
        return
    old_room = record["room"]
    print(f"  {record['name']} is now in room {old_room}.")
    print("  Rooms with a free bed:")
    if show_free_rooms(rooms, allotments, old_room) == 0:
        print("    (none) - no other room has a free bed.")
        return
    new_no = read_text("Move to room number: ").upper()
    new_room = find_room(rooms, new_no)
    if new_room is None:
        print("  That room does not exist.")
    elif new_no == old_room:
        print("  The student is already in that room.")
    elif free_beds(new_room, allotments) == 0:
        print("  That room has no free bed.")
    else:
        record["room"] = new_no
        save_allotments(allotments)
        print(f"  {record['name']} moved from {old_room} to {new_no}.")
        try_waiting_list(rooms, allotments, waiting)


def vacancy_report(rooms, allotments):
    print("\n--- Vacancies and occupancy ---")
    if len(rooms) == 0:
        print("  There are no rooms yet.")
        return
    print(f"  {'Block':<7}{'Single':>8}{'Double':>8}{'Triple':>8}{'Free':>7}{'Beds':>7}{'Occupancy':>12}")
    vacancy_parts = []
    occupancy_parts = []
    for block in get_blocks(rooms):
        free_by_type = {"Single": 0, "Double": 0, "Triple": 0}
        capacity = 0
        used = 0
        for room in rooms:
            if room["block"] != block:
                continue
            capacity += room["cap"]
            used += count_in_room(allotments, room["no"])
            free_by_type[room["type"]] += free_beds(room, allotments)
        total_free = free_by_type["Single"] + free_by_type["Double"] + free_by_type["Triple"]
        percent = 0.0
        if capacity > 0:
            percent = round(used * 100 / capacity, 1)
        print(f"  {block:<7}{free_by_type['Single']:>8}{free_by_type['Double']:>8}"
              f"{free_by_type['Triple']:>8}{total_free:>7}{capacity:>7}{percent:>11}%")
        vacancy_parts.append(f"Block {block}: {total_free} beds")
        occupancy_parts.append(f"Block {block}: {percent}%")
    print("\n  Vacancies - " + " | ".join(vacancy_parts))
    print("  Occupancy - " + " | ".join(occupancy_parts))


def search_student(rooms, allotments, waiting):
    print("\n--- Search a student ---")
    reg = read_reg("Register number: ")
    record = find_allotment(allotments, reg)
    if record is None:
        person = find_waiting(waiting, reg)
        if person is not None:
            print(f"  {person['name']} ({person['year']} year) has no room yet and is on the waiting list.")
        else:
            print("  No student found with that register number.")
        return
    room = find_room(rooms, record["room"])
    if room is None:
        print(f"  {record['name']} is listed in room {record['room']}, but that room is missing from rooms.txt.")
        return
    print(f"  {record['name']} ({record['year']} year) - Room {room['no']}, "
          f"Block {room['block']}, Floor {room['floor']} ({room['type']})")
    found = False
    for other in allotments:
        if other["room"] == room["no"] and other["reg"] != reg:
            print(f"  Roommate: {other['name']} ({other['year']} year)")
            found = True
    if not found:
        print("  No roommates in this room.")


def list_rooms(rooms, allotments):
    print("\n--- All rooms ---")
    if len(rooms) == 0:
        print("  There are no rooms yet.")
        return
    for room in rooms:
        used = count_in_room(allotments, room["no"])
        print(f"  {room['no']} | Block {room['block']} | Floor {room['floor']} | "
              f"{room['type']} | {used}/{room['cap']} beds filled")
        for record in allotments:
            if record["room"] == room["no"]:
                print(f"       - {record['name']} ({record['reg']}, {record['year']} year)")


def show_waiting(waiting):
    print("\n--- Waiting list ---")
    if len(waiting) == 0:
        print("  The waiting list is empty.")
        return
    print("  Shown in the order beds will be given (first years first):")
    number = 1
    for person in sorted(waiting, key=year_rank):
        block = person["block"]
        rtype = person["type"]
        if block == "":
            block = "any"
        if rtype == "":
            rtype = "any"
        print(f"  {number}. {person['name']} ({person['reg']}, {person['year']} year) "
              f"- wants block: {block}, type: {rtype}")
        number += 1


# ------------------------------------------------------------
# main menu
# ------------------------------------------------------------

def show_menu():
    print("\n==========================================")
    print("        HOSTEL ROOM ALLOCATION")
    print("==========================================")
    print(" 1. Add a room")
    print(" 2. Allot a student")
    print(" 3. Vacate a student")
    print(" 4. Transfer a student")
    print(" 5. Vacancies and occupancy by block")
    print(" 6. Search a student")
    print(" 7. View all rooms")
    print(" 8. View waiting list")
    print(" 0. Exit")


def main():
    rooms = load_rooms()
    allotments = load_allotments()
    waiting = load_waiting()
    print(f"Loaded {len(rooms)} rooms, {len(allotments)} allotments "
          f"and {len(waiting)} students on the waiting list.")
    running = True
    while running:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_room(rooms, allotments, waiting)
        elif choice == "2":
            allot_student(rooms, allotments, waiting)
        elif choice == "3":
            vacate_student(rooms, allotments, waiting)
        elif choice == "4":
            transfer_student(rooms, allotments, waiting)
        elif choice == "5":
            vacancy_report(rooms, allotments)
        elif choice == "6":
            search_student(rooms, allotments, waiting)
        elif choice == "7":
            list_rooms(rooms, allotments)
        elif choice == "8":
            show_waiting(waiting)
        elif choice == "0":
            print("All changes are saved. Goodbye!")
            running = False
        else:
            print("  Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed. Saved data is safe.")
