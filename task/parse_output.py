def output(orders: list, output_file: str = "output.txt"):
    with open(output_file, "w") as f:
        for idx, vec in enumerate(orders):
            if idx != 0:
                f.write("\n")
            for idy, ride in enumerate(vec):
                if idy == 0:
                    f.write(str(ride))
                else:
                    f.write(" " + str(ride))


def write_output(items, output_file):
    with open(output_file, 'w') as fd:
        for orders in items:
            fd.write('%s %s\n' % (len(orders), ' '.join(orders)))
