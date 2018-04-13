#!/usr/bin/env python3


import re
from subprocess import check_output


def find_trackpoint():
    out = check_output(["xinput", "list"]).decode("utf-8")
    return re.search(r"TrackPoint\s+?id=(\d+)", out)[1]


def find_prop(device_id, props):
    ret = []
    out = check_output(["xinput", "list-props", device_id]).decode("utf-8")
    for line in out.splitlines():
        for prop in props:
            m = re.search(r"{}\s\((\d+)\):\s+?([\d|,|\s]+)".format(prop), line)
            if m:
                ret.append((m[1], list(map(int, m[2].split(",")))))
    return ret


def set_prop(dev, prop, *value):
    check_output(["xinput", "set-prop", dev, prop] + list(map(str, value)))


def main():
    from sys import argv
    dev_id = find_trackpoint()
    (speed_id, _), (profile_id, profile_enabled) = \
            find_prop(dev_id, ["Accel Speed", "Accel Profile Enabled"])

    def change_to_adaptive():
        set_prop(dev_id, speed_id, 0.2)
        set_prop(dev_id, profile_id, 1, 0)

    def change_to_flat():
        set_prop(dev_id, speed_id, 1)
        set_prop(dev_id, profile_id, 0, 1)

    if argv[1] == "adaptive":
        change_to_adaptive()
    elif argv[1] == "flat":
        change_to_flat()
    elif argv[1] == "toggle":
        if profile_enabled == [0, 1]:
            change_to_adaptive()
        elif profile_enabled == [1, 0]:
            change_to_flat()


if __name__ == '__main__':
    main()
