REQUIRED_FIELDS = set("byr.iyr.eyr.hgt.hcl.ecl.pid".split('.'))

def is_valid_height(height: str) -> bool:
    unit = height[-2:].lower()
    height = height[:-2]
    if height.isdigit():
        height = int(height)
        if unit == 'cm':
            return 150 <= height <= 193
        elif unit == 'in':
            return 59 <= height <= 76
    return False        


def is_valid_hair_colour(clr: str) -> bool:
    HEXDIGITS = set("0123456789abcdef")
    if clr.startswith('#'):
        clr = clr[1:]
        if len(clr) == 6:
            return all(char in HEXDIGITS for char in clr)
    return False


def is_valid_eye_colour(clr: str) -> bool:
    VALID_COLOURS = "amb.blu.brn.gry.grn.hzl.oth".split('.')
    return clr in VALID_COLOURS


def is_valid_passport_id(pid: str) -> bool:
    return len(pid) == 9 and pid.isdigit()


def is_all_fields_valid(ppt: dict) -> bool:
    valid =  (
        # Birth year
        1920 <= int(ppt['byr']) <= 2002
        # Issue year
        , 2010 <= int(ppt['iyr']) <= 2020
        # Expiration year
        , 2020 <= int(ppt['eyr']) <= 2030
        # Height rules are hard
        , is_valid_height(ppt['hgt'])
        # Hair colour rules slightly better
        , is_valid_hair_colour(ppt['hcl'])
        # Eye colour rules better
        , is_valid_eye_colour(ppt['ecl'])
        # Passport ID cool and good
        , is_valid_passport_id(ppt['pid'])
    )
    return all(valid)

def is_valid_passport(passport: dict) -> bool:
    enough_fields = all(field in passport for field in REQUIRED_FIELDS)
    return (enough_fields and is_all_fields_valid(passport))

def populate_passport(line: str, passport: dict) -> None:
    for group in line.split():  # Groups are separated by whitespace
        key, val = group.split(':', maxsplit=1)
        passport[key] = val

n_valid = 0
passport = dict()

with open("day4.in", 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            populate_passport(line, passport)
        else:           # Blank lines separate passports
            if is_valid_passport(passport):
                n_valid += 1
            passport.clear()
# In case it doesn't end in a blankline
if is_valid_passport(passport):
    n_valid += 1

print(n_valid)