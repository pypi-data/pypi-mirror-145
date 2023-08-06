import os
import sys
import argparse
import pandas as pd
import numpy as np
from distutils.util import strtobool


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='restidy -i < resfinder4.0_result_directory > -o < output_file_directory > \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')
    parser.add_argument("-i", help="<input_path>: resfinder_result_path")
    parser.add_argument("-o", help="<output_file_path>: output_file_path")
    parser.add_argument("-p", default=True, help="True of False to process point mutation results",
                        type=lambda x: bool(strtobool(str(x).lower())))
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='Display version')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def cate_mapping_dict(file):
    """
    create mapping dict {"gene"=>"Resistance Category"}
    """
    df_map = pd.read_csv(file, names=['Database', 'Gene'], sep='\t')
    mapping_dict = dict(zip(df_map['Gene'], df_map['Database']))
    return mapping_dict


def drug_mapping_dict(file):
    """
    create mapping dict {"gene"=>"Antibiotics"}
    """
    df_drug = pd.read_csv(file, sep='\t')
    drug_dict = dict(zip(df_drug['Gene'], df_drug['Phenotype'].str.lower()))
    return drug_dict


def join(f):
    """
    Get the path of database file which was located in the scripts dir
    """
    return os.path.join(os.path.dirname(__file__), f)


def res_concate(path):
    """
    process resfinder results to long dataframe
    """
    df_resistance_final = pd.DataFrame()
    # print(path)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            resistance_file = os.path.join(
                file_path, 'ResFinder_results_tab.txt')
            if os.path.isfile(resistance_file):
                # print(resistance_file)
                df_resistance_tmp = pd.read_csv(resistance_file, sep='\t')
                df_resistance_tmp['Strain'] = file
                df_resistance_final = pd.concat(
                    [df_resistance_final, df_resistance_tmp])
    return df_resistance_final


def point_concate(path):
    """
    process pointfinder results to long dataframe
    """
    df_point_final = pd.DataFrame()
    # print(path)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            point_file = os.path.join(file_path, 'PointFinder_results.txt')
            if os.path.isfile(point_file):
                # print(point_file)
                df_point_tmp = pd.read_csv(point_file, sep='\t')
                df_point_tmp['Strain'] = file
                df_point_final = pd.concat([df_point_final, df_point_tmp])
    df_point_final['AMR'] = df_point_final['Mutation'].replace(
        r' .*', r'', regex=True)
    df_point_final['Identity'] = 100
    return df_point_final


def resistance_count(df_resistance, df_point):
    """
    count the number of isolates resistance to different drugs
    df_resistance should cotain the drugs column
    """
    df1 = df_resistance[['Strain', 'Resistance gene', 'Drugs']].copy()
    df1.rename(columns={'Resistance gene': 'AMR'}, inplace=True)
    df1.reset_index(drop=True, inplace=True)
    df1_index = df1['Drugs'].str.split(', ', expand=True).stack(
    ).to_frame().reset_index(level=1, drop=True)
    df1_tmp = df1.join(df1_index).rename(columns={0: 'Drug'})
    # print(df1_tmp)
    # Generate long style dataframe contains strain, drug, AMR
    if not len(df_point.index) == 0:
        df2 = df_point[['Strain', 'Mutation', 'Resistance']].copy()
        df2.rename(columns={'Mutation': 'AMR',
                            'Resistance': 'Drugs'}, inplace=True)
        df2.reset_index(drop=True, inplace=True)
        df2_index = df2['Drugs'].str.lower().str.split(',', expand=True).stack(
        ).to_frame().reset_index(level=1, drop=True)
        df2_tmp = df2.join(df2_index).rename(columns={0: 'Drug'})
        # print(df2_tmp)
        df3 = pd.concat([df1_tmp, df2_tmp])
    else:
        df3 = df1_tmp
    # df3.drop_duplicates(inplace=True)
    # df3.to_csv('test.csv', index=False)
    df3_tmp = df3.groupby(['Strain', 'Drug'])['Drug'].size(
    ).to_frame().rename(columns={'Drug': 'Count'})
    df3_tmp.reset_index(inplace=True)
    # print(df3_tmp)
    df4 = df3_tmp.pivot_table(index='Strain', columns='Drug', values='Count')
    df4[df4.notna()] = 1
    df_drug_pivot = df4.copy()
    df_rr_count = df4.sum().to_frame().rename(
        columns={0: 'No. of resistance isolates'})

    # Create concatenate drugs with every isolates(Strain)
    df_drugs_concat = df3.groupby('Strain')['Drug'].apply(
        lambda x: ','.join(x.unique())).reset_index()

    return df_drug_pivot, df_rr_count, df_drugs_concat


def long_db_arg(df_resistance, df_point):
    """
    concat the acquired genes and point mutation genes
    """
    df1 = df_resistance[['Strain', 'Resistance gene',
                         'Identity', 'Database']].copy()
    df1.rename(columns={'Resistance gene': 'AMR'}, inplace=True)
    df1.reset_index(drop=True, inplace=True)
    if not len(df_point.index) == 0:
        df2 = df_point[['Strain', 'AMR', 'Identity', 'Database']].copy()
        df2.reset_index(drop=True, inplace=True)
        df3 = pd.concat([df1, df2])
    else:
        df3 = df1
    df3.loc[df3['Database'].isnull(), 'Database'] = 'Unknown'
    return df3


def amr_concatenate(df_resistance, df_point):
    """
    get concatenated AMR string
    """
    df1 = df_resistance[['Strain', 'Resistance gene']].copy()
    df1.rename(columns={'Resistance gene': 'AMR'}, inplace=True)
    if not len(df_point.index) == 0:
        df2 = df_point[['Strain', 'Mutation']].copy()
        df2.rename(columns={'Mutation': 'AMR'}, inplace=True)
        df2['AMR'].replace(r' .*', r'', regex=True, inplace=True)
        df3 = pd.concat([df1, df2])
    else:
        df3 = df1
    df_amr_concat = df3.groupby('Strain')['AMR'].apply(
        lambda x: ','.join(x.unique())).reset_index()
    # Get the number of ARGs
    df_amr_concat['NUM_of_AMRs'] = df_amr_concat['AMR'].str.split(
        ',').str.len()
    df_amr_statistic = df_amr_concat[['Strain', 'NUM_of_AMRs', 'AMR']].copy()
    return df_amr_statistic


def main():
    args = args_parse()
    input_path = args.i
    input_path = os.path.abspath(input_path)

    # check if the output directory exists
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    # create output files handler
    output_file_path = os.path.abspath(args.o)
    output_resistance_file = os.path.join(
        output_file_path, 'resfinder_sum.csv')
    output_point_file = os.path.join(output_file_path, 'point_sum.csv')
    drug_output_file = os.path.join(output_file_path, 'drug_pivot.csv')
    resis_count_file = os.path.join(
        output_file_path, 'resistance_statistic.csv')
    combined_pattern_file = os.path.join(
        output_file_path, 'pattern_process.csv')
    long_style_file = os.path.join(
        output_file_path, 'AMR_concat_long.csv')
    summary_pivot_file = os.path.join(
        output_file_path, 'summary_pivot.csv')

    # print info
    print('The results will be write into following files:\n')
    print(f'The resistance summary file is saved to {output_resistance_file}')
    if args.p:
        print(f"The point summary file is saved to {output_point_file}")
    else:
        print("You choose do not process point mutation results")
    print(f'The pivot table style file is saved to {drug_output_file}')
    print(
        f'The drug resistance statistic file is saved to {resis_count_file}')
    print(
        f'The pattern of unique AMRs and Drugs of each isolates is saved to {combined_pattern_file}')
    print(
        f'The long style of AMRs is saved to {long_style_file }')
    print(
        f'The summary pivot table is saved to {summary_pivot_file}')

    # Get the directory of script and read mapping file
    cate_mapping_file = join("gene_db_mapping.tsv")
    cate_map_dict = cate_mapping_dict(cate_mapping_file)

    # process drugs parsing method
    drug_mapping_file = join("gene_drugs_mapping.tsv")
    drug_map_dict = drug_mapping_dict(drug_mapping_file)

    df_resistance = res_concate(input_path)

    # Generate acquired resistance genes dataframe with drugs column
    df_resistance['Drugs'] = df_resistance['Resistance gene'].map(
        drug_map_dict)

    # mapping resistance gene to database
    df_resistance['Database'] = df_resistance['Resistance gene'].map(
        cate_map_dict)

    # Generate the pivot table acquired resistance genes
    df_resistance_final = df_resistance.pivot_table(index='Strain', columns=[
        'Database', 'Resistance gene'], values='Identity', aggfunc=lambda x: ','.join(map(str, x)))

    # today codes
    if args.p:
        df_point = point_concate(input_path)
        df_point['Database'] = df_point['AMR'].map(cate_map_dict)
        # Process point mutation results
        df_point_final = df_point.groupby(['Strain'])['Mutation'].apply(
            lambda x: ','.join(x)).to_frame()
        df_point_final.to_csv(output_point_file)
    else:
        df_point = pd.DataFrame()

    long_df = long_db_arg(df_resistance, df_point)
    long_df.to_csv(long_style_file, index=False)

    arg_sum_pivot = long_df.pivot_table(index='Strain', columns=[
        'Database', 'AMR'], values='Identity', aggfunc=lambda x: ','.join(map(str, x)))

    # Generate the pivot table of drugs which combined with acquired and mutation resistance genes
    df_pivot_drugs, df_rr_statistics, df_drugs_concat = resistance_count(
        df_resistance, df_point)

    # Get unique pattern of AMR and Drugs in every isolates
    df_amr_concat = amr_concatenate(df_resistance, df_point)
    df_combined_pattern = df_amr_concat.merge(
        df_drugs_concat, on='Strain', how='outer')

    # print(df_final)
    df_resistance_final.to_csv(output_resistance_file)
    arg_sum_pivot.to_csv(summary_pivot_file)
    df_pivot_drugs.to_csv(drug_output_file)
    df_rr_statistics.to_csv(resis_count_file)
    df_combined_pattern.to_csv(combined_pattern_file, index=False)


if __name__ == '__main__':
    main()
