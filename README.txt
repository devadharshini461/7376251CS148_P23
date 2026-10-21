Name           : Devadharshini S
Register No    : 7376251IT148
Project        : P23 - Hostel Room Allocation

FILES IN THIS FOLDER
main.py          the complete program
rooms.txt        RoomNo|Block|Floor|Type|Capacity           (12 sample rooms)
allotment.txt    RoomNo|RegNo|Name|Year                     (22 sample records)
waiting.txt      RegNo|Name|Year|PreferredBlock|PreferredType (empty at start)
sample_run.txt   terminal session showing every feature working
README.txt       this file

If a data file is missing the program starts with empty data and creates
the file when something is saved.

FEATURES COMPLETED (required)
1. Add rooms with room number, block, floor, type (Single/Double/Triple)
   and capacity. Capacity cannot be more than the beds of that type.
2. Allot a student (register number, name, year) to a room with a free bed.
   The preferred block and type are used first. If they are full, the program
   tries the block only, then the type only, then any room, and tells the
   warden how well the preference was matched.
3. One student can never be allotted to two rooms.
4. Vacate a student, and transfer a student to another room with a free bed.
5. Vacancies by block and type (table) and the occupancy percentage of each
   block, also printed as one line like the sample in the project document.
6. Search a student by register number to see the room and the roommates.
Extra menu option: view all rooms with the students inside them.

BONUS FEATURES DONE
- Waiting list. If no bed is free, the student can be put on the waiting list.
  When a bed becomes free (vacate, transfer or new room) the waiting students
  are allotted automatically, first years first, and students of the same year
  in the order they joined.

NOTES
- Data is saved to the text files after every change.
- The | character is not allowed in any input.
- Wrong menu choices, letters instead of numbers, empty input and values out of
  range show a message and ask again.
- Year can be typed as I, II, III, IV or as 1 to 4.

KNOWN PROBLEMS
- None known. Room numbers and block names are saved in capital letters.
