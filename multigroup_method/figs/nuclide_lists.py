import tables as tb

from char.iso_track import transmute
from char.envchar import iso_list_conversions, serpent_xs_isos_available, \
                         serpent_mt_avaliable, temperature_flag

from isoname import zzLL
from metasci.nuke import nuc_data

def latex_nuclide(nuc):
    """Takes a nuclide in zzaaam and converts it to the appropriate LaTeX string."""
    elem = zzLL[nuc/10000].capitalize()
    anum = (nuc%10000)/10
    meta = (0 < nuc%10)

    ln = "\\nuc{{{0}}}{{{1}}}".format(elem, anum)
    if meta:
        ln += "\\superscript{*}"

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

        # Split up table nicely onto multiple pages
        if (nrow not in [0, len(nuclides)/ncol - 1]) and (nrow%40 == 0):
            table += "\\hline\n"
            table += "\\end{tabular}\n"
            table += "\n"
            table += "\\begin{{tabular}}{{|{0}|}}\n".format('c'*ncol)
            table += "\\hline\n"

    table += "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\end{center}\n"
    table += "\end{table}\n"

    with open(label + '.tex', 'w') as f:
        f.write(table)


mtmap = {
        1: '$t$',
        2: '$e$',
        4: '$i$',
        16: '$2n$',
        17: '$3n$',
        18: '$f$',
        19: '$f19$',
        20: '$f20$',
        21: '$f21$',
        38: '$f38$',
        27: '$a$',
        102: '$\\gamma$',
        103: '$p$',
        104: '$d$',
        105: '$\\nuc{H}{3}$',
        106: '$\\nuc{He}{3}$',
        107: '$\\alpha$',
        }
#mtmap.update({50+i: '$i{0}$'.format(i) for i in range(1, 41)})
mtmap.update({50+i: '$i{0}$'.format(i) for i in range(1, 6)})
mtkeys = set(mtmap.keys())

def mt_reaction_table(nuclides, xsdata, temp, title=""):
    nuclides = sorted(nuclides)
    temp_flag = temperature_flag(temp)
    label = title.lower().replace(" ", "_")
    mts = serpent_mt_avaliable(xsdata, nuclides, temp_flag)

    table = ("\\begin{table}[htbp]\n"
             "\\begin{center}\n")
    table += "\\caption{{{0}}}\n".format(title)
    table += "\\label{{{0}}}\n".format(label)
    table += "\\begin{tabular}{|l|c|}\n"
    table += "\\hline\n"
    table += "\\textbf{nuclides} & \\textbf{reactions} \\\\\n"
    table += "\\hline\n"

    for i, nuc in enumerate(nuclides):
        nuc_la = latex_nuclide(nuc)
        reactions = sorted(mts[nuc] & mtkeys)
        rx_la = ", ".join([mtmap[rx] for rx in reactions])
        table += "{0} & {1} \\\\\n".format(nuc_la, rx_la)

        # Split up table nicely onto multiple pages
        if (i not in [0, len(nuclides) - 1]) and (i%40 == 0):
            table += "\\hline\n"
            table += "\\end{tabular}\n"
            table += "\n"
            table += "\\begin{tabular}{|l|c|}\n"
            table += "\\hline\n"
            table += "\\textbf{nuclides} & \\textbf{reactions} \\\\\n"
            table += "\\hline\n"

    table += "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\end{center}\n"
    table += "\end{table}\n"

    with open(label + '.tex', 'w') as f:
        f.write(table)


def make_tables(nuclides, xsdata, temp=600):
    # Get the canonical form of the nuclides
    nuclides_conv = iso_list_conversions(nuclides)
    nuclides_zz = set(nuclides_conv['zzaaam'])

    serp_nuc_avialable = serpent_xs_isos_available(xsdata)
    nuclides_in_serp = nuclides_zz & serp_nuc_avialable
    nuclides_not_in_serp = nuclides_zz - serp_nuc_avialable

    with tb.openFile(nuc_data, 'r') as nd:
        decay_nuclides = set(nd.root.decay.cols.from_iso_zz[:])
        decay_nuclides.update(nd.root.decay.cols.to_iso_zz[:])

    nuclides_not_modeled = decay_nuclides - nuclides_zz
    
    nuclide_latex_table(nuclides_in_serp, "Nuclides Calculated via Serpent")
    nuclide_latex_table(nuclides_not_in_serp, "Nuclides Calculated via Models")
    nuclide_latex_table(nuclides_not_modeled, "Nuclides Calculated via Interpolation")

    mt_reaction_table(nuclides_in_serp, xsdata, temp, "Reactions Available in Serpent")


if __name__ == '__main__':
    xsdata = "/usr/share/serpent/xsdata/endf7.xsdata"
    make_tables(transmute, xsdata)
