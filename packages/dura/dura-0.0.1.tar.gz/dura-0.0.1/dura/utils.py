#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wes Apr 6 14:29:26 2022

@author: zdx
"""
import numpy as np
import pandas as pd
import os
import multiprocessing
from multiprocessing import Pool
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
from rdkit.Chem.Scaffolds.MurckoScaffold import GetScaffoldForMol
from rdkit.Chem.Scaffolds import MurckoScaffold
from moses.metrics import mol_passes_filters, QED, SA, logP
from functools import partial
from rdkit.Chem import rdinchi
from os.path import basename, splitext, join, dirname
from glob import glob
from tqdm import tqdm

def GetFileSuffix(path):
    """
    >>> suffix = GetFileSuffix(path)
    """
    return os.path.splitext(os.path.basename(path))[1]

def read_df(file, sep=None, index_col=None, header=0):
    """
    >>> df = read_df(file)
    """
    if GetFileSuffix(file) == '.xlsx':
        if index_col is not None:
            df = pd.read_excel(file, index_col=index_col)
        else:
            df = pd.read_excel(file)
    else:
        with open(file, 'r') as f:
            line = f.readline().strip()
        if '\t' in line:
            sep = '\t'
        elif ',' in line:
            sep = ','
        elif ' ' in line:
            sep = ' '
        else:
            print('Can not recognize what the separator is. please provide it'
                  ' by add argument "sep" ')
            return
        if index_col is not None:
            df = pd.read_csv(file, index_col=index_col, sep=sep, header=header)
        else:
            df = pd.read_csv(file, sep=sep, header=header)
    return df

def autoFindsmile(df):
    cols = df.columns
    for col in cols:
        if isinstance(col, str):
            try:
                mol = Chem.MolFromSmiles(df[col][0])
            except:
                mol = None
            if mol is not None:
                print(mol)
                df.rename(columns={col:'SMILES'}, inplace=True)
    return df

"""
Remove duplicates molecules
"""
def drop_duplicate_mols(file=None, df=None, out=None, sep=None, header=None, 
                              col_names=None, inplace=False, save_out=True,
                              remain_InChI=True, donothing=False):
    """
    file = '/y/Aurora/Fernie/data/ligand_based_data/DUD-E/aa2ar.csv'
    """
    if file is not None:
        if splitext(basename(file))[1] == '.smi':
            if sep is None and header is None:
                sep = ' '
                header = None
            df = pd.read_csv(file, sep = sep, header = header)
            if col_names is not None:
                df.columns = col_names
            elif df.shape[1] == 1:
                df.columns = ['SMILES']
            elif df.shape[1] == 2:
                df.columns = ['SMILES', 'ID']
            else:
                print(f'{file} columns names is not given.')
                return
        else:
            if sep is not None and header is not None:
                df = read_df(file, sep = sep, header = header)
            else:
                df = read_df(file)

    df = autoFindsmile(df)
    
    if donothing:
        print('Just read raw file and do nothing.')
        return df

    elif df is None:
        print('please check your input.')
        return
    
    if 'SMILES' not in df.columns:
        print('The file must have have SMILES column.')
        return
    
    if 'label' in df.columns:
        df.sort_values(by='label', ascending = False, inplace=True)
    
    print('Before:', df.shape[0], 'moleculs.')
    
    if 'InChI' not in df.columns:
        df = SMILES2mol2InChI(df)
    else:
        print('Already have InChI')
    df.drop_duplicates('InChI', inplace=True)
    
    print('After drop duplicates:', df.shape[0], 'moleculs.')

    if not remain_InChI:
        del df['InChI']

    if save_out:
        if out is not None:
            df.to_csv(out, index=False)
        elif file is not None:
            if inplace:
                out = file
            else:
                file_dir = dirname(file)
                file_name, suffix = splitext(basename(file))
                file_name = file_name + '_drop_duplicates'
                out = join(file_dir, ''.join([file_name, suffix]))
        else:
            print('Not given a output path.')
            return
        if splitext(basename(out))[1] == '.smi':
            if 'InChI' in df.columns:
                del df['InChI']
        if splitext(basename(out))[1] == '.smi':
            header=False
        df.to_csv(out, index=False)
        if inplace:
            print(f'Success to replace raw input file {out}.\n')
        else:
            print(f'Success to save out to {out}.\n')
    return df

def drop_multi_files_duplicate_mols(files=None, input_dir=None, 
                                    output_dir = None,
                                    suffix=None, donothing=False,
                                    sep=None, header=None, 
                                    col_names=None, inplace=True, 
                                    save_out=True, remain_InChI=True):
    """
    input_dir = '/y/Aurora/Fernie/data/ligand_based_data/MUV'
    drop_multi_files_duplicate_mols(input_dir=input_dir, suffix='csv')
    """
    if suffix == 'smi':
        sep = ' '
        header = None
    
    if files is None and input_dir is not None:
        files = glob(join(input_dir, f'*.{suffix}'))
    else:
        print('Please check your input.')
        return
    dfs = []
    failed = []
    for file in tqdm(files):
        try:
            df = drop_duplicate_mols(file=file, sep=sep, header=header, 
                                  col_names=col_names, inplace=inplace, 
                                  save_out=save_out, remain_InChI=remain_InChI,
                                  donothing=donothing)
            dfs.append(df)
        except:
            failed.append(file)
        
    print(failed)
    return dfs

def merge_files(files=None, input_dir=None, out=None, suffix='csv', donothing=True):
    """
    input_dir = '/y/Aurora/Fernie/data/ligand_based_data/MUV'
    out = '/y/Aurora/Fernie/data/ligand_based_data/MUV.csv'
    merge_files(input_dir=input_dir, out=out)
    """
    if files is None and input_dir is not None:
        dfs = drop_multi_files_duplicate_mols(input_dir=input_dir, 
            suffix=suffix, donothing=donothing)
        df = pd.concat(dfs)
        df = drop_duplicate_mols(df=df, out=out)
        return df
    else:
        print('Please check your input.')
        return

"""
=========================== parallelize apply =================================
"""

def parallelize_dataframe(df, func, **kwargs):
    CPUs = multiprocessing.cpu_count()

    num_partitions = int(CPUs*0.8) # number of partitions to split dataframe
    num_cores = int(CPUs*0.8) # number of cores on your machine

    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    func = partial(func, **kwargs)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def judge_whether_is_dir(path):
    if not os.path.isdir(path):
        return False
    else:
        return True

def remain_path_of_dir(x):
    return list(filter(judge_whether_is_dir, x))

"""
-------------------------------------------------------------------------------
String to mol 
-------------------------------------------------------------------------------
"""
def InChI2MOL(inchi):
    try:
        mol = Chem.inchi.MolFromInchi(inchi)
        if not mol == None:
            return mol
        else:
            return np.nan
    except:
        return np.nan
    
def SMILES2MOL(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol == None:
            return mol
        else:
            return np.nan
    except:
        return np.nan

"""
-------------------------------------------------------------------------------
Apply string to mol
-------------------------------------------------------------------------------
"""
def apply_SMILES2MOL(df):
    df['ROMol'] = df['SMILES'].apply(SMILES2MOL)
    return df

def apply_InChI2MOL(df):
    df['ROMol'] = df['InChI'].apply(InChI2MOL)
    return df

"""
-------------------------------------------------------------------------------
Mol to string
-------------------------------------------------------------------------------
"""
def MOL2SMILES(mol):
    try:
        sm = Chem.MolToSmiles(mol)
        return sm
    except:
        return np.nan

def MOL2InChI(mol):
    try:
        inchi, retcode, message, logs, aux = rdinchi.MolToInchi(mol)
        return inchi
    except:
        return np.nan

def MOL2ECFP4(mol, nbits=2048, radius=2, useFeatures=False):
    try:
        res = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, 
                                                    nBits=nbits, 
                                                    useFeatures=useFeatures)
        return np.array(res)
    except:
        return np.nan

"""
-------------------------------------------------------------------------------
apply mol to string
-------------------------------------------------------------------------------
"""
def apply_MOL2SMILES(df):
    df['SMILES'] = df.ROMol.apply(MOL2SMILES)
    return df

def apply_MOL2InChI(df):
    df['InChI'] = df.ROMol.apply(MOL2InChI)
    return df

def apply_mol2ECFP4(df, nbits=2048, radius=2, useFeatures=False):
    # mol2ECFP4V2 = partial(MOL2ECFP4, nbits=nbits, radius=radius)
    df['ECFP4'] = df['ROMol'].apply(MOL2ECFP4, nbits=nbits, radius=radius,
                                    useFeatures=useFeatures)
    return df

"""
-------------------------------------------------------------------------------
Parallel convert from one molecular respresentation to another.
-------------------------------------------------------------------------------
"""

def add_mol(df):
    if 'SMILES' in df.columns:
        df = parallelize_dataframe(df, apply_SMILES2MOL)
    elif 'InChI' in df.columns:
        df = parallelize_dataframe(df, apply_InChI2MOL)
    df.dropna(inplace=True)
    return df

def add_ECFP4(df, **kwargs):
    if 'ROMol' not in df.columns:
        df = add_mol(df)
    df = parallelize_dataframe(df, apply_mol2ECFP4, **kwargs)
    df.dropna(inplace=True)
    del df['ROMol']
    return df

def add_inchi(df):
    if 'ROMol' not in df.columns:
        df = add_mol(df)
    df = parallelize_dataframe(df, apply_MOL2InChI)
    del df['ROMol']
    return df
    
def InChI2mol2SMILES(df):
    if 'ROMol' not in df.columns:
        df = parallelize_dataframe(df, apply_InChI2MOL)
    df = parallelize_dataframe(df, apply_MOL2SMILES)
    del df['ROMol']
    return df

def SMILES2mol2InChI(df):
    if 'ROMol' not in df.columns:
        df = parallelize_dataframe(df, apply_SMILES2MOL)
    df = parallelize_dataframe(df, apply_MOL2InChI)
    del df['ROMol']
    return df

"""
-------------------------------------------------------------------------------
Property functions
-------------------------------------------------------------------------------
"""
def judge_whether_has_rings_4(mol):
    r = mol.GetRingInfo()
    if len([x for x in r.AtomRings() if len(x)==4]) > 0:
        return False
    else:
        return True
    
def add_whether_have_4_rings(data):
    """4 rings"""
    data['4rings'] = data['ROMol'].apply(judge_whether_has_rings_4)
    return data

def four_rings_filter(df):
    df = parallelize_dataframe(df, add_whether_have_4_rings)
    df = df[df['4rings']==True]
    del df['4rings']
    return df

def MW(mol):
    try:
        res = Chem.Descriptors.ExactMolWt(mol)
        return res
    except:
        return np.nan

def HBA(mol):
    try:
        res = Chem.rdMolDescriptors.CalcNumHBA(mol)
        return res
    except:
        return np.nan

def HBD(mol):
    try:
        res = Chem.rdMolDescriptors.CalcNumHBD(mol)
        return res
    except:
        return np.nan

def TPSA(mol):
    try:
        res = Chem.rdMolDescriptors.CalcTPSA(mol)
        return res
    except:
        return np.nan

def NRB(mol):
    try:
        res =  Chem.rdMolDescriptors.CalcNumRotatableBonds(mol)
        return res
    except:
        return np.nan
    
def get_num_rings(mol):
    try:
        r = mol.GetRingInfo()
        res = len(r.AtomRings())
        return res
    except:
        return np.nan

def get_num_rings_6(mol):
    try:
        r = mol.GetRingInfo()
        res = len([x for x in r.AtomRings() if len(x) > 6])
        return res
    except:
        return np.nan

def LOGP(mol):
    try:
        res = logP(mol)
        return res
    except:
        return np.nan
    
def MCF(mol):
    """
    Keep molecules whose MCF=True
    MCF=True means toxicity. but toxicity=True is not bad if the patient is dying.
    """
    try:
        res = mol_passes_filters(mol)
        return res
    except:
        return np.nan

def synthesis_availability(mol):
    """
    0-10. smaller, easier to synthezie.
    not very accurate.
    """
    try:
        res = SA(mol)
        return res
    except:
        return np.nan
    
def estimation_drug_likeness(mol):
    """
    0-1. bigger is better.
    """
    try:
        res = QED(mol)
        return res
    except:
        return np.nan

def get_scaffold_mol(mol):
    try: 
        res = GetScaffoldForMol(mol)
        return res
    except:
        return np.nan

def add_atomic_scaffold_mol(df):
    df['atomic_scaffold_mol'] = df.ROMol.apply(get_scaffold_mol)
    return df

def get_scaffold_inchi(mol):
    try: 
        scaffold_mol = GetScaffoldForMol(mol)
        inchi = MOL2InChI(scaffold_mol)
        return inchi
    except:
        return np.nan

def get_scaffold_smiles(mol):
    try: 
        scaffold_mol = GetScaffoldForMol(mol)
        smiles = MOL2SMILES(scaffold_mol)
        return smiles
    except:
        return np.nan

def add_scaffold_inchi(df):
    df['scaffold_inchi'] = df.ROMol.apply(get_scaffold_inchi)
    return df

def add_descriptors(df, pro=['MW', 'logP', 'HBA', 'HBD', 
                             'TPSA', 'NRB', 'MCF', 'SA', 'QED',
                             'rings', 'scaffold_inchi', 'scaffold_smiles']):
    if 'MW' in pro:
        df['MW'] = df.ROMol.apply(MW)
    if 'logP' in pro:
        df['logP'] = df.ROMol.apply(LOGP)
    if 'HBA' in pro:
        df['HBA'] = df.ROMol.apply(HBA)
    if 'HBD' in pro:
        df['HBD'] =  df.ROMol.apply(HBD)
    if 'TPSA' in pro:
        df['TPSA'] = df.ROMol.apply(TPSA)
    if 'NRB' in pro:
        df['NRB'] = df.ROMol.apply(NRB)
    if 'MCF' in pro:
        df['MCF'] = df.ROMol.apply(MCF)
    if 'SA' in pro:
        df['SA'] = df.ROMol.apply(synthesis_availability)
    if 'QED' in pro:
        df['QED'] = df.ROMol.apply(estimation_drug_likeness)
    if 'rings' in pro:
        df['rings'] = df.ROMol.apply(get_num_rings)
    if 'scaffold_inchi' in pro:
        df['scaffold_inchi'] = df.ROMol.apply(get_scaffold_inchi)
    if 'scaffold_smiles' in pro:
        df['scaffold_smiles'] = df.ROMol.apply(get_scaffold_smiles)
    return df

def validity_filter(df):
    print("Start to remove invalid SMILES...")
    if "ROMol" not in df.columns:
        df = parallelize_dataframe(df, apply_SMILES2MOL)
        df.dropna(subset=['ROMol'], inplace=True)
    print("Finished.")
    return df

def add_features(df, remove_na=False):
    if "ROMol" not in df.columns:
        df = validity_filter(df)
    df = parallelize_dataframe(df, add_descriptors)
    df.dropna(subset=['MW', 'logP', 'HBA', 'HBD', 
                            'TPSA', 'NRB', 'MCF', 'SA', 'QED',
                            'rings', 'scaffold_inchi', 'scaffold_smiles'],
                inplace=True)
    return df