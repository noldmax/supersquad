#! /usr/bin/env python
"Parse Player Data and Generate Optimal Lineups"

import re
import argparse

#==============================================================================
# Global Variables
#==============================================================================

valid_positions = {"PG", "SG", "SF", "PF", "C"}

MAX_POSITIONS = 5

#------------------------------------------------------------------------------
# Global dictionary mapping each valid position to a list of
# PlayerData entries.
#
# Example of what the ultimate filled in structure might look like:
#   {"PG": [PlayerData0, PlayerData1], "SG": [PlayerData2]}
#------------------------------------------------------------------------------
position_lists = {} 

all_lineups = []

SALARY_CAP = 60000


#==============================================================================
# Classes
#==============================================================================

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class PlayerData:
    name = ""
    cost = 0
    pts = 0.0

    def __init__(self, name, cost, pts):
        self.name = name
        self.cost = cost
        self.pts = pts

class Lineup:
    name = ""
    cost = 0
    pts = 0.0

    def __init__(self, name, cost, pts):
        self.name = name
        self.cost = cost
        self.pts = pts

#==============================================================================
# Functions
#==============================================================================

def get_args():
    """Parse Player Data and Generate Optimal Lineups"""
    parser = argparse.ArgumentParser(description='Parse player data, produce '
                                     + 'optimal lineup')
    parser.add_argument('-i', '--input', default='playerdata',
                        help='input playerdata file (in format from iphone ' +
                        'notes)')
    parser.add_argument('-o', '--output', action='store_true',
                        default='pokersheet.xls', help='output xls file ' +
                        'containing poker data')
    return parser.parse_args()

#------------------------------------------------------------------------------
# generate_lineups
#   Generate lineups
#------------------------------------------------------------------------------
def generate_lineups():
    pos_index = 0
    get_player
    for pos in position_lists.keys():
        for pdata in position_lists[pos]
            lineup = []
            lineup.append(pdata)
            if not is_lineup_valid()
                continue 

#------------------------------------------------------------------------------
# print_all_lists
#   Print all position lists to stdout
#------------------------------------------------------------------------------
def print_all_lists():
    for pos in position_lists.keys():
        print pos + ':'
        for pdata in position_lists[pos]:
            print "  ", pdata.name, pdata.cost, pdata.pts
    print "\n"

#==============================================================================

#------------------------------------------------------------------------------
# is_valid_position
#   Check whether the provided position is valid.
#
# params:
#   position   Position string to test for validity
#
# return:
#   True if valid; False if non-valid
#------------------------------------------------------------------------------
def is_valid_position(position):
    if (position in valid_positions):
        return True
    else:
        return False

#==============================================================================

#------------------------------------------------------------------------------
# add_entry
#   Populate the position list(s) with name and price of the player
#
# params:
#   name        Player name string
#   cost        Cost of this player
#   positions   Player's positions, separated by "/"
#   points      Player's projected fantasy points
#------------------------------------------------------------------------------
def add_entry(name, cost, positions, points):

    #----------------------------------------------------------------------
    # Sort by position
    #----------------------------------------------------------------------
    position_list = positions.split("/");

    for pos in position_list:
        #----------------------------------------------------------------------
        # Test that position is valid
        #----------------------------------------------------------------------
        if not is_valid_position(pos):
            print "Invalid position " + pos + "supplied. Ignoring"

        #----------------------------------------------------------------------
        # We have a valid position. Create a new PlayerData object and add it
        # to the list for that position.
        #----------------------------------------------------------------------
        position_lists[pos].append(PlayerData(name, cost, points))

#==============================================================================

#------------------------------------------------------------------------------
# process_file
#   Read file entries into player entry lists
#
# params:
#   in_file   File to read player data from
#------------------------------------------------------------------------------
def process_file(in_file):
    #--------------------------------------------------------------------------
    # Read the lines of the file into flines
    #--------------------------------------------------------------------------
    flines = in_file.readlines()

    for line in flines:
        #----------------------------------------------------------------------
        # Split each line into 3 entries:
        #   1. player name
        #   2. player price
        #   3. player position(s)
        #
        # If line format is invalid, skip to the next line
        #----------------------------------------------------------------------
        if len(line.split(" ")) == 4:
            name, price, position, points = line.split(" ")
        else:
            print "Line formatted incorrectly:"
            print line
            continue

        #----------------------------------------------------------------------
        # Add to list of entries
        #----------------------------------------------------------------------
        add_entry(name, price, position, points)

#==============================================================================

#------------------------------------------------------------------------------
# initialize_lists
#   Create empty lists for each valid position
#------------------------------------------------------------------------------
def initialize_lists():
   for position in valid_positions:
        #----------------------------------------------------------------------
        # Add a dictionary key for each position and map it to an empty list
        # that will contain the PlayerData entries
        #----------------------------------------------------------------------
        position_lists[position] = []

#==============================================================================
# Python Main
#==============================================================================

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------
args = get_args()

#------------------------------------------------------------------------------
# Grab the input file content
#------------------------------------------------------------------------------
input_file = open(args.input)

#------------------------------------------------------------------------------
# Initialize player lists
#------------------------------------------------------------------------------
initialize_lists()

#------------------------------------------------------------------------------
# Parse entries in the input file
#------------------------------------------------------------------------------
process_file(input_file)

#------------------------------------------------------------------------------
# Print all entries
#------------------------------------------------------------------------------
print_all_lists()

#------------------------------------------------------------------------------
# Generate possible valid lineups
#------------------------------------------------------------------------------
generate_lineups()
