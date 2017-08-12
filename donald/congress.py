import json


def add_congress_data(dest, *args):
    with open('congress.json', 'r') as jin:
        jdata = json.load(jin)
        congressdata = []

        for j in range(0, len(args), 2):
            i = 0
            while i < len(jdata):
                dparent = ""
                dchild = ""
                dparent = args[j]
                dchild = args[j + 1]
                # dchild = 'district' if dchild is 'district' else 'state'
                try:
                    member = jdata[i][dparent][dchild].strip().replace(
                        ".", "").replace(', ', ' ').strip()
                except TypeError as e:
                    try:
                        termnumber = int(len(jdata[i][dparent]) - 1)
                        member = jdata[i][dparent][termnumber][
                            dchild].strip().replace(".", "").replace(', ', ' ').strip()
                    except KeyError as e:
                        member = 'N/A'
                    except AttributeError as e:
                        member = str(jdata[i][dparent][termnumber][dchild]).strip(
                        ).replace(".", "").replace(', ', ' ').strip()

                congressdata.append(member)
                i += 1
        with open(dest, 'r') as huntin:
            linels = huntin.readline().strip().replace(', ', ',').replace(
                ', Jr', ' Jr').replace(', Sr', ' Sr').strip().split(',')
            hunters = list(congressdata + linels)
            with open(dest, 'w') as huntout:
                huntout.write(','.join(hunters).strip())
                huntout.close()


add_congress_data('thehunters.txt', 'name', 'official_full', 'terms', 'type',
                  'terms', 'party', 'terms', 'state', 'terms', 'district', 'terms', 'phone')


def get_wikipedia_data(name=str):
    