from char.envchar import iso_list_conversions, serpent_xs_isos_available
from char.iso_track import transmute

def nuclide_latex_table(nuclides):
    nuclides = sorted(nuclides)

    for ncol in range(10, 0, -1):
        if len(nuclides)%ncol == 0:
            break

def make_tables(nuclides, xsdata):
    # Get the canonical form of the nuclides
    nuclides_conv = iso_list_conversions(nuclides)
    nuclides_zz = set(nuclides_conv['zzaaam'])

    serp_nuc_avialable = serpent_xs_isos_available(xsdata)
    nuclides_in_serp = nuclides_zz & serp_nuc_avialable
    nuclides_not_in_serp = nuclides_zz - serp_nuc_avialable


if __name__ == '__main__':
    xsdata = "/usr/share/serpent/xsdata/endf7.xsdata"
    make_tables(transmute, xsdata)
