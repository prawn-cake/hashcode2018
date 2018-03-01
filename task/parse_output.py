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
