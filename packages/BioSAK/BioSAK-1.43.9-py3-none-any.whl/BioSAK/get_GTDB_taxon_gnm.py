import argparse
import os

get_GTDB_taxon_gnm_parser_usage = '''
================================== get_GTDB_taxon_gnm example commands ==================================

# Example commands
BioSAK get_GTDB_taxon_gnm -meta bac120_metadata_r202.tsv -path genome_paths.tsv -taxon taxons.txt
BioSAK get_GTDB_taxon_gnm -meta ar122_metadata_r202.tsv -path genome_paths.tsv -taxon taxons.txt

# -meta: bac120_metadata_r202.tsv or ar122_metadata_r202.tsv
# -path: genome_paths.tsv, in fastani folder from auxillary_files
# -taxon: one taxon per line, example below:
p__Thermoproteota
c__Methanosarcinia
f__Thalassarchaeaceae

=====================================================================================================
'''


def get_GTDB_taxon_gnm(args):

    gtdb_gnm_metadata =         args['meta']
    gtdb_ref_gnm_path_txt =     args['path']
    taxons_to_retrieve_txt =    args['taxon']
    output_prefix =             args['p']

    gnms_to_retrieve_gtdb_txt = '%s_in_GTDB.txt'        % output_prefix
    gnms_to_retrieve_ncbi_txt = '%s_in_NCBI.txt'        % output_prefix
    gnms_taxonomy_txt         = '%s_genome_taxon.txt'   % output_prefix

    already_exist_files = []
    for each_op in [gnms_to_retrieve_gtdb_txt, gnms_to_retrieve_ncbi_txt, gnms_taxonomy_txt]:
        if os.path.isfile(each_op) is True:
            already_exist_files.append(each_op)

    if len(already_exist_files) > 0:
        print('The following files already exist, use a different prefix with -p')
        print('\n'.join(already_exist_files))
        print('Program exited!')
        exit()

    # read in taxons_to_retrieve_txt
    taxons_to_retrieve_set = set()
    for each_taxon in open(taxons_to_retrieve_txt):
        taxons_to_retrieve_set.add(each_taxon.strip())

    # read in gtdb_ref_gnm_path_txt
    gtdb_ref_gnm_set = set()
    for each_gnm_path in open(gtdb_ref_gnm_path_txt):
        gnm_path_split = each_gnm_path.strip().split(' ')
        gnm_accession = gnm_path_split[0].split('_genomic')[0]
        gtdb_ref_gnm_set.add(gnm_accession)

    # get genomes from interested taxons
    gnm_set_to_retrieve = set()
    gnm_to_taxon_dict = {}
    col_index = {}
    for each_ref in open(gtdb_gnm_metadata):
        each_ref_split = each_ref.strip().split('\t')
        if each_ref.startswith('accession	ambiguous_bases'):
            col_index = {key: i for i, key in enumerate(each_ref_split)}
        else:
            ref_accession = each_ref_split[0][3:]
            gtdb_taxonomy = each_ref_split[col_index['gtdb_taxonomy']]
            for each_interested_taxon in taxons_to_retrieve_set:
                if each_interested_taxon in gtdb_taxonomy:
                    gnm_set_to_retrieve.add(ref_accession)
                    gnm_to_taxon_dict[ref_accession] = gtdb_taxonomy

    # write out
    from_gtdb = 0
    from_ncbi = 0
    gnms_taxonomy_txt_handle = open(gnms_taxonomy_txt, 'w')
    gnms_to_retrieve_gtdb_txt_handle = open(gnms_to_retrieve_gtdb_txt, 'w')
    gnms_to_retrieve_ncbi_txt_handle = open(gnms_to_retrieve_ncbi_txt, 'w')
    for each_gnm_to_retrieve in sorted([i for i in gnm_set_to_retrieve]):
        gnm_taxon = gnm_to_taxon_dict.get(each_gnm_to_retrieve, 'NA')
        gnms_taxonomy_txt_handle.write('%s\t%s\n' % (each_gnm_to_retrieve, gnm_taxon))
        if each_gnm_to_retrieve in gtdb_ref_gnm_set:
            gnms_to_retrieve_gtdb_txt_handle.write('%s\n' % each_gnm_to_retrieve)
            from_gtdb += 1
        else:
            gnms_to_retrieve_ncbi_txt_handle.write('%s\n' % each_gnm_to_retrieve)
            from_ncbi += 1
    gnms_taxonomy_txt_handle.close()
    gnms_to_retrieve_gtdb_txt_handle.close()
    gnms_to_retrieve_ncbi_txt_handle.close()

    gnms_to_retrieve_gtdb_txt_with_num = '%s_in_GTDB_%s.txt'        % (output_prefix, from_gtdb)
    gnms_to_retrieve_ncbi_txt_with_num = '%s_in_NCBI_%s.txt'        % (output_prefix, from_ncbi)

    os.system('mv %s %s' % (gnms_to_retrieve_gtdb_txt, gnms_to_retrieve_gtdb_txt_with_num))
    os.system('mv %s %s' % (gnms_to_retrieve_ncbi_txt, gnms_to_retrieve_ncbi_txt_with_num))

    print('Total number of genomes from interested taxons: %s'  % len(gnm_set_to_retrieve))
    print('Genomes in GTDB: %s, see details in %s'              % (from_gtdb, gnms_to_retrieve_gtdb_txt_with_num))
    print('Genomes in NCBI: %s, see details in %s'              % (from_ncbi, gnms_to_retrieve_ncbi_txt_with_num))
    print('Genome taxon information is in %s'                   % (gnms_taxonomy_txt))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-meta',        required=True,                      help='GTDB reference genome metadata')
    parser.add_argument('-path',        required=True,                      help='GTDB genome_paths.tsv')
    parser.add_argument('-taxon',       required=True,                      help='interested taxons, one taxon per line')
    parser.add_argument('-p',           required=False, default='Genomes',  help='output prefix')
    args = vars(parser.parse_args())
    get_GTDB_taxon_gnm(args)
