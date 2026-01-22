from pprint import pprint
# Master Caskets Goal
master_casket_goal = 176550

# Gather Rates /hour
hard_gather = 21.6
elite_gather = 17.9 * 0.99
master_gather = 17.9 * 0.01

bik_hard = 4.3
bik_elite = 4.7
bik_master = 0.17

# Solve Rates /hour
hard_solve_rate = 67
elite_solve_rate = 39
master_solve_rate = 35

# Master and OSH Rates /casket including rerolls
master_scroll_per_easy = (1/50) * (4/3)
master_scroll_per_medium = (1/30) * (4/3)
master_scroll_per_hard = (1/15) * (4/3) # 0.08888888
master_scroll_per_elite = (1/5) * (4/3) # 0.26666666

osh_easy_per_medium = (1/80) * (4/3)
osh_medium_per_hard = (1/90) * (4/3)
osh_hard_per_elite = (1/90) * (4/3)
osh_elite_per_master = (1/100) * (4/3)

#####################################
# Touch below code at your own risk #
#####################################

# Process
# 1. Gather from menaphos market guards w/bik
# 2. Solve hards and elites w/bik then buying elite scrolls from tt points
# 3. Open hards and elites w/osh
# 4. Solve masters w/bik
# 5. Open masters w/osh
# 6. Repeat step 2 - step 5 until below significant figure threshold
# 7. Return to step 1

# Code
total_time = 0.0
totals_dict={
    # Note that masters are counting caskets, since that is our ultimate goal
    "gather_time": 0,
    "total_time": 0,
    "total_hard_scrolls": 0,
    "total_elites_scrolls": 0,
    "total_masters_caskets": 0
}
carrier={
    "hard_scrolls": 0,
    "elite_scrolls": 0,
    "master_scrolls": 0,

    "hard_caskets": 0,
    "elite_caskets": 0,
    "master_caskets": 0,
}

def gather_clues(gather_time):
    carrier["hard_scrolls"] += (hard_gather + bik_hard) * gather_time
    carrier["elite_scrolls"] += (elite_gather + bik_elite) * gather_time
    carrier["master_scrolls"] += (master_gather + bik_master) * gather_time

    totals_dict["total_time"] += gather_time
    totals_dict["gather_time"] += gather_time

def solve_hards_elites():
    hards = carrier["hard_scrolls"]
    elites = carrier["elite_scrolls"]

    # Calculate solve time
    hard_solve_time = hards / hard_solve_rate
    elite_solve_time = elites / elite_solve_rate
    solve_time = hard_solve_time + elite_solve_time
    totals_dict["total_time"] += solve_time

    # Calculate treasure trail points for elite scroll buying purposes
    tt_points = hards * 5.008 + elites * 10.016

    # Add caskets to carrier including LotD 1% double chance
    totals_dict["total_hard_scrolls"] += hards
    carrier["hard_caskets"] += hards * 1.01
    totals_dict["total_elites_scrolls"] += elites
    carrier["elite_caskets"] += elites * 1.01

    # Zero-out hard and elite scrolls. Then buy elite scrolls and add bik time to all
    carrier["hard_scrolls"] = solve_time * bik_hard
    carrier["elite_scrolls"] = (solve_time * bik_elite) + (tt_points / 100)
    carrier["master_scrolls"] += solve_time * bik_master

def solve_masters():
    # Calculate solve time
    solve_time = carrier["master_scrolls"] / master_solve_rate
    totals_dict["total_time"] += solve_time

    # Calculate treasure trail points for elite scroll buying purposes
    tt_points = carrier["master_scrolls"] * 20.032

    # Add caskets to carrier including LotD 1% double chance
    carrier["master_caskets"] += carrier["master_scrolls"] * 1.01

    # Zero-out master scrolls. Then buy elite scrolls and add bik time to all
    carrier["hard_scrolls"] += solve_time * bik_hard
    carrier["elite_scrolls"] += (solve_time * bik_elite) + (tt_points / 100)
    carrier["master_scrolls"] = solve_time * bik_master

def open_clues():
    totals_dict["total_masters_caskets"] += carrier["master_caskets"]
    # Open master caskets for osh elite caskets
    carrier["elite_caskets"] += carrier["master_caskets"] * osh_elite_per_master

    # Open elite caskets for master scrolls & osh hard caskets
    carrier["master_scrolls"] += carrier["elite_caskets"] * master_scroll_per_elite
    carrier["hard_caskets"] += carrier["elite_caskets"] * osh_hard_per_elite
    
    # Open hard caskets for master scrolls & osh medium caskets
    carrier["master_scrolls"] += carrier["hard_caskets"] * master_scroll_per_hard
    medium_caskets = carrier["hard_caskets"] * osh_medium_per_hard

    # Open medium caskets for master scrolls & osh easy caskets
    carrier["master_scrolls"] += medium_caskets * master_scroll_per_medium
    easy_caskets = medium_caskets * osh_easy_per_medium

    # Open easy caskets for master scrolls
    carrier["master_scrolls"] += easy_caskets * master_scroll_per_easy

    # Zero-out casket counts
    carrier["hard_caskets"] = 0
    carrier["elite_caskets"] = 0
    carrier["master_caskets"] = 0

while totals_dict["total_masters_caskets"] < master_casket_goal:
    gather_clues(1)
    while carrier["elite_scrolls"] > 1:
        solve_hards_elites()
        open_clues()
        # pprint(carrier, sort_dicts=False)
        while carrier["master_scrolls"] > 1:
            solve_masters()
            open_clues()
            # pprint(carrier, sort_dicts=False)

print("Total Time (Hours): ",totals_dict["total_time"])
pprint(totals_dict, sort_dicts=False)
