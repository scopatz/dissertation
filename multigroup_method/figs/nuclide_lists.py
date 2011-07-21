from char.envchar import iso_list_conversions, serpent_xs_isos_available
from char.iso_track import transmute
from isoname import zzLL

def latex_nuclide(nuc):
    """Takes a nuclide in zzaaam and converts it to the appropriate LaTeX string."""
    elem = zzLL[nuc/10000].capitalize()
    anum = (nuc%10000)/10
    meta = (0 < nuc%10)

    ln = "\\nuc{{{0}}}{{{1}}}".format(elem, anum)
    if meta:
        ln += "^*"

    return ln


def nuclide_latex_table(nuclides, title=""):
    nuclides = sorted(nuclides)
    nuclides = [latex_nuclide(nuc) for nuc in nuclides]
    label = title.lower().replace(" ", "_")

    for ncol in range(10, 0, -1):
        if len(nuclides)%ncol == 0:
            break

    table = ("\\begin{table}[htbp]\n"
             "\\begin{center}\n")
    table += "\\caption{{{0}}}\n".format(title)
    table += "\\label{{{0}}}\n".format(label)
    table += "\\begin{{tabular}}{{|{0}|}}\n".format('c'*ncol)
    table += "\\hline\n"

    for nrow in range(len(nuclides)/ncol):
        table += " & ".join(nuclides[nrow*ncol:(nrow+1)*ncol])
        table += " \\\\\n"

    table += "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\end{center}\n"
    table += "\end{table}\n"

    with open(label + '.tex', 'w') as f:
        f.write(table)


def make_tables(nuclides, xsdata):
    # Get the canonical form of the nuclides
    nuclides_conv = iso_list_conversions(nuclides)
    nuclides_zz = set(nuclides_conv['zzaaam'])

    serp_nuc_avialable = serpent_xs_isos_available(xsdata)
    nuclides_in_serp = nuclides_zz & serp_nuc_avialable
    nuclides_not_in_serp = nuclides_zz - serp_nuc_avialable

    nuclide_latex_table(nuclides_in_serp, "Nuclides Calculated via Serpent")
    nuclide_latex_table(nuclides_not_in_serp, "Nuclides Calculated via Models")


if __name__ == '__main__':
    xsdata = "/usr/share/serpent/xsdata/endf7.xsdata"
    make_tables(transmute, xsdata)
