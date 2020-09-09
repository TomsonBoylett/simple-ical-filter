import argparse
from icalendar import Calendar

def parse_args():
    parser = argparse.ArgumentParser(description='Takes local ical file and filters events to \
                                                  those containing provided phrases')
    parser.add_argument('-n', '--negate', dest='negate', action='store_true',
                        help='Filter to events not containing provided phrases')
    parser.add_argument('-a', '--and', dest='ands', action='store_true',
                        help='Evaluate each event against multiple phrases using "and" instead of "or"')
    parser.add_argument('-d', '--description', dest='description', action='store_true',
                        help='Also search description of each event')
    parser.add_argument('-o', '--output', dest='output', action='store', default='output.ics', help='Path to output ical file')
    parser.add_argument('input', action='store', help='Path to ical file')
    parser.add_argument('phrase', nargs='+', help='String to find within each event')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    with open(args.input, 'rb') as f:
        calendar = Calendar.from_ical(f.read())

    filtered = Calendar()

    for component in calendar.walk():
        keys = {'SUMMARY'}
        if args.description:
            keys.add('DESCRIPTION')
        keys = keys.intersection(component.keys())

        if not keys:
            continue

        all_matches = []
        for k in keys:
            field = component[k].lower()
            is_match = [phrase in field for phrase in args.phrase]
            is_match = all(is_match) if args.ands else any(is_match)
            all_matches.append(is_match)
        
        all_matches = any(all_matches)
        if args.negate:
            all_matches = not all_matches
        if all_matches:
            filtered.add_component(component)
            print({k: str(v.to_ical(), encoding='UTF-8') for k, v in component.items() if hasattr(v, 'to_ical')})
    
    with open(args.output, 'wb') as f:
        f.write(filtered.to_ical())
        
