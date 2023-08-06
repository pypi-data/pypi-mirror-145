import pandas as pd
import matplotlib.pyplot as plt
import time
import pymzml
import scipy.signal
from numpy import where, argmin, median, std, zeros, argmax, mean
from numba import jit
from numba.typed import Dict
from numba.typed import List
from glob import glob
import numpy as np
import scipy.interpolate as interpolate
import multiprocessing as mp
from molmass import Formula
import os
import json
import shutil
import sys
from tqdm import tqdm
from collections import Counter
import re
import copy
import networkx as nx
from multiprocessing import Pool

atom_mass_table = pd.Series(
    data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
          'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
          'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
          'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
          'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
          })

def peak_picking(df1, ms_error=50, threshold=15, i_threshold=200):
    '''
    Perform peak picking for a whole LC-MS file, and return the result.
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param ms_error: The ms difference between two selected masses (for extraction), this parameter may not affect the final result, but 50 is recommended.
    :param threshold: This parameter is used for the function of peak_finding(eic, threhold)
    :return:
    '''
    index = ms_locator(df1, ms_error)  ### 获得ms locator
    start_t = time.time()
    RT = np.array(df1.columns)
    l = len(index)
    num = 0
    num_p = 0
    data = []
    for i in tqdm(range(l - 1), desc='Finding peaks'):
        df2 = df1.iloc[index[i]:index[i + 1]]
        a = np.array(df2).T  ### 将dataframe转换成np.array
        if len(a[0]) != 0:  ### 判断切片结果是否为0
            extract_c = a.sum(axis=1)
            peak_index, left, right = peak_finding(extract_c, threshold)  ## 关键函数，峰提取
            if len(peak_index) != 0:  ### 判断是否找到峰
                df3 = df2[df2.columns[peak_index]]
                rt = np.round(RT[peak_index], 2)
                intensity = np.round(np.array(df3.max().values), 0)
                mz = np.round(np.array(df3.idxmax().values), 4)
                name = 'peak' + str(num_p)
                locals()[name] = np.array([rt, mz, intensity]).T
                data.append(locals()[name])

    peak_info = np.concatenate(data)
    peak_info_df = pd.DataFrame(data=peak_info, columns=['rt', 'mz', 'intensity'])
    peak_all = peak_info_df[peak_info_df['intensity'] > i_threshold]
    peak_all = peak_all.sort_values(by='intensity').reset_index(drop=True)
    return peak_all


def ms_locator(df1, ppm=50):
    '''
    For pick picking, selecting a series of mass locators for 50-1000.
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param ppm: the mass difference between two locators
    :return: mass locators
    '''

    @jit(nopython=True)
    def find_locator(list1, error):
        locators = []
        locator = list1[0]
        for i in range(len(list1)):
            if list1[i] > locator:
                locators.append(i)
                locator *= (1 + error * 1e-6)
        return locators

    ms_list = list(df1.index)
    typed_a = List()
    [typed_a.append(x) for x in ms_list]
    locators = find_locator(typed_a, ppm)
    return locators


def sep_scans(path, company):
    '''
    To separate scans for MS1, MS2.
    :param path: The path for mzML files
    :return: ms1, ms2 and lockspray
    '''
    if company == 'Waters':
        run = pymzml.run.Reader(path)
        ms1, ms2 = [], []
        for scan in tqdm(run, desc='Separating ms1 and ms2'):
            if scan.id_dict['function'] == 1:
                ms1.append(scan)
            if scan.ms_level == 2:
                ms2.append(scan)
        return ms1, ms2
    else:
        run = pymzml.run.Reader(path)
        ms1, ms2 = [], []
        for scan in tqdm(run, desc='Separating ms1 and ms2'):
            if scan.ms_level == 1:
                ms1.append(scan)
            else:
                ms2.append(scan)
        return ms1, ms2


def peak_finding(eic, threshold=15):
    '''
    finding peaks in a single extracted chromatogram,and return peak index, left valley index, right valley index.
    :param eic: extracted ion chromatogram data; e.g., [1,2,3,2,3,1...]
    :param threshold: define the noise level for a peak, 6 is recommend
    :return:peak index, left valley index, right valley index.
    '''
    peaks, _ = scipy.signal.find_peaks(eic, width=2)
    prominence = scipy.signal.peak_prominences(eic, peaks)
    peak_prominence = prominence[0]
    left = prominence[1]
    right = prominence[2]
    ### peak_picking condition 1: value of peak_prominence must be higher than
    len_pro = len(peak_prominence)
    if len(peak_prominence) == 0:
        peak_index, left, right = np.array([]), np.array([]), np.array([])
    else:
        median_1 = np.median(peak_prominence)  ### 获得中位数的值
        index_pos2 = where(prominence[0] > threshold * median_1)[0]
        peak_index = peaks[index_pos2]
        left = left[index_pos2]
        right = right[index_pos2]
    return peak_index, left, right


def extract(df1, mz, error=50):
    '''
    Extracting chromatogram based on mz and error.
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param mz: Targeted mass for extraction.
    :param error: mass error for extraction
    :return: rt,eic
    '''
    low = mz * (1 - error * 1e-6)
    high = mz * (1 + error * 1e-6)
    low_index = argmin(abs(df1.index.values - low))
    high_index = argmin(abs(df1.index.values - high))
    df2 = df1.iloc[low_index:high_index]
    rt = df1.columns.values
    if len(np.array(df2)) == 0:
        intensity = np.zeros(len(df1.columns))
    else:
        intensity = np.array(df2).T.sum(axis=1)
    return rt, intensity  ### 只返回RT和EIC


def extract2(df1, mz, error=50):
    '''
    Extracting chromatogram based on mz and error.
    :param df1: LC-MS dataframe, genrated by the function gen_df(),or ms1 scans can be imported.
    :param mz: Targeted mass for extraction.
    :param error: mass error for extraction
    :return: rt,eic
    '''
    if type(df1) == pd.core.frame.DataFrame:
        low = mz * (1 - error * 1e-6)
        high = mz * (1 + error * 1e-6)
        low_index = argmin(abs(df1.index.values - low))
        high_index = argmin(abs(df1.index.values - high))
        df2 = df1.iloc[low_index:high_index]
        rt = df1.columns.values
        if len(np.array(df2)) == 0:
            intensity = np.zeros(len(df1.columns))
        else:
            intensity = np.array(df2).T.sum(axis=1)
    elif type(df1) == list:
        rt = []
        intensity = []
        low = mz * (1 - error * 1e-6)
        high = mz * (1 + error * 1e-6)
        for scan in df1:
            mz_all = scan.mz
            i_all = scan.i
            rt1 = scan.scan_time[0]
            rt.append(rt1)
            index_e = np.where((mz_all <= high) & (mz_all >= low))
            eic1 = 0 if len(index_e[0]) == 0 else i_all[index_e[0]].sum()
            intensity.append(eic1)
    return rt, intensity  ### 只返回RT和EIC


def gen_df_to_centroid(ms1, ms_round=4):
    '''
    Convert mzml data to a dataframe in centroid mode.
    :param ms1: ms scan list generated by the function of sep_scans(), or directed from pymzml.run.Reader(path).
    :return: A Dataframe
    '''
    t1 = time.time()
    l = len(ms1)
    num = 0
    print('\r Generating dataframe...             ', end="")
    ###将所有的数据转换成centroid格式，并将每个scan存在一个独立的变量scan(n)中
    data = []
    for i in tqdm(range(l)):
        name = 'scan' + str(i)
        peaks, _ = scipy.signal.find_peaks(ms1[i].i.copy())
        locals()[name] = pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(ms_round),
                                   name=round(ms1[i].scan_time[0], 3))
        data.append(locals()[name])
    ## 开始级联所有数据
    print('\r Concatenating all the data...                   ', end="")
    df1 = pd.concat(data, axis=1)
    df2 = df1.fillna(0)
    t4 = time.time()
    t = round(t4 - t1, 2)
    print(f'\r Concat finished, Consumed time: {t} s            ', end='')
    return df2


def gen_df_raw(ms1, ms_round=4):
    '''
    Convert mzml data to a dataframe in profile mode.
    :param ms1: ms scan list generated by the function of sep_scans(), or directed from pymzml.run.Reader(path).
    :return: A Dataframe
    '''
    t1 = time.time()
    l = len(ms1)
    ###将每个scan存在一个独立的变量scan(n)中
    data = []
    for i in tqdm(range(l), desc='Reading each scans'):
        name = 'scan' + str(i)
        locals()[name] = pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round), name=round(ms1[i].scan_time[0], 3))
        data.append(locals()[name])
    ### 将所有的变量汇总到一个列表中
    ## 开始级联所有数据
    print('\r Concatenating all the data...                             ', end="")
    df1 = pd.concat(data, axis=1)
    df2 = df1.fillna(0)
    t4 = time.time()
    t = round(t4 - t1, 2)
    print(f'\r Concat finished, Consumed time: {t} s                     ', end='')
    return df2


def B_spline(x, y):
    '''
    Generating more data points for a mass peak using beta-spline based on x,y
    :param x: mass coordinates
    :param y: intensity
    :return: new mass coordinates, new intensity
    '''
    t, c, k = interpolate.splrep(x, y, s=0, k=4)
    N = 300
    xmin, xmax = x.min(), x.max()
    new_x = np.linspace(xmin, xmax, N)
    spline = interpolate.BSpline(t, c, k, extrapolate=False)
    return new_x, spline(new_x)


def cal_bg(data):
    '''
    :param data: data need to calculate the background
    :return: background value
    '''
    if len(data) > 5:
        Median = median(data)
        Max_value = max(data)
        STD = std(data)
        Mean = mean(data)
        if Median == 0:
            bg = Mean + STD
        elif Mean <= Median * 3:
            bg = Max_value
        elif Mean > Median * 3:
            bg = Median
    else:
        bg = 1000000
    return bg + 1


def peak_checking_plot(df1, mz, rt1, Type='profile', path=None):
    '''
    Evaluating/visulizing the extracted mz
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param mz: Targetd mass for extraction
    :param rt1: expected rt for peaks
    :return:
    '''

    fig = plt.figure(figsize=(12, 4))
    ### 检查色谱图ax
    ax = fig.add_subplot(121)
    rt, eic = extract(df1, mz, 50)
    rt2 = rt[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    eic2 = eic[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    ax.plot(rt2, eic2)
    ax.set_xlabel('Retention Time(min)', fontsize=12)
    ax.set_ylabel('Intensity', fontsize=12)
    peak_index = np.argmin(abs(rt - rt1))
    peak_height = max(eic[peak_index - 2:peak_index + 2])
    ax.scatter(rt1, peak_height * 1.05, c='r', marker='*', s=50)
    ##计算背景
    cut = int(len(eic2) / 3)
    bg_left, bg_right = cal_bg(eic2[:cut]), cal_bg(eic2[-cut:])
    rt3 = rt2[:cut]
    rt4 = rt2[-cut:]
    bg1 = zeros(cut) + bg_left
    bg2 = zeros(cut) + bg_right
    ax.plot(rt3, bg1)
    ax.plot(rt4, bg2)
    SN1 = round(peak_height / bg_left, 1)
    SN2 = round(peak_height / bg_right, 1)
    ax.set_title(f'SN_left:{SN1},         SN_right:{SN2}')
    ax.set_ylim(top=peak_height * 1.1, bottom=-peak_height * 0.05)

    ### 检查质谱图ax1
    ax1 = fig.add_subplot(122)
    width = 0.02
    spec = spec_at_rt(df1, rt1)  ## 提取到特定时间点的质谱图
    new_spec = target_spec(spec, mz, width=0.04)

    if Type == 'profile':
        mz_obs, error1, mz_opt, error2, resolution = evaluate_ms(new_spec, mz)
        ax1.plot(new_spec)
        ax1.bar(mz_obs, max(new_spec.values), color='r', width=0.0005)
        ax1.bar(mz_opt, max(new_spec.values), color='g', width=0.0005)
        ax1.text(min(new_spec.index.values) + 0.005, max(new_spec.values) * 0.8,
                 f'mz_obs: {mz_obs},{error1} \n mz_opt:{mz_opt}, {error2}')
    else:
        ax1.bar(mz, max(new_spec.values), width=0.0002)

    ax1.set_title(f'mz_exp: {mz}')
    ax1.set_xlabel('m/z', fontsize=12)
    ax1.set_ylabel('Intensity', fontsize=12)
    ax1.set_xlim(mz - 0.05, mz + 0.05)

    if path == None:
        pass
    else:
        plt.savefig(path, dpi=1000)
        plt.close('all')


def peak_alignment(files_excel, rt_error=0.1, mz_error=0.015):
    '''
    Generating peaks information with reference mz/rt pair
    :param files_excel: files for excels of peak picking and peak checking;
    :param rt_error: rt error for merge
    :param mz_error: mz error for merge
    :return: Export to excel files
    '''
    print('\r Generating peak reference...        ', end='')
    peak_ref = gen_ref(files_excel, rt_error=rt_error, mz_error=mz_error)
    pd.DataFrame(peak_ref, columns=['rt', 'mz']).to_excel(
        os.path.join(os.path.split(files_excel[0])[0], 'peak_ref.xlsx'))
    j = 1
    for file in tqdm(files_excel,desc='Reading each excel files'):
        peak_p = pd.read_excel(file, index_col='Unnamed: 0').loc[:, ['rt', 'mz']].values
        peak_df = pd.read_excel(file, index_col='Unnamed: 0')
        new_all_index = []
        for i in range(len(peak_p)):
            rt1, mz1 = peak_p[i]
            index = np.where((peak_ref[:, 0] <= rt1 + rt_error) & (peak_ref[:, 0] >= rt1 - rt_error)
                             & (peak_ref[:, 1] <= mz1 + mz_error) & (peak_ref[:, 1] >= mz1 - mz_error))
            new_index = str(peak_ref[index][0][0]) + '_' + str(peak_ref[index][0][1])
            new_all_index.append(new_index)
        peak_df['new_index'] = new_all_index
        peak_df = peak_df.set_index('new_index')
        peak_df.to_excel(file.replace('.xlsx', '_alignment.xlsx'))


def peak_checking(peak_df, df1, error=50, profile=True,
                  i_threshold=200, SN_threshold=3):
    '''
    Processing extracted peaks, remove those false positives.
    :param peak_df: Extracted peaks generated by the function of peak_picking
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param error: For the function of extract(df,mz, error)
    :param i_threshold: filter peaks with intensity<i_threshold
    :param SN_threshold: filter peaks with sn<SN_threshold
    :return:
    '''
    if profile == True:

        final_result = pd.DataFrame()
        peak_num = len(peak_df['rt'])
        SN_all_left, SN_all_right, area_all, mz_obs_all, mz_opt_all, resolution_all = [], [], [], [], [], []
        for i in tqdm(range(peak_num), desc='Checking each peaks'):
            mz = peak_df.iloc[i]['mz']
            rt = peak_df.iloc[i]['rt']
            ### 第一步：处理色谱峰
            rt_e, eic_e = extract(df1, mz, error=error)
            peak_index = np.argmin(abs(rt_e - rt))  ## 找到特定时间点的索引
            rt_left = rt - 3
            rt_right = rt + 3
            peak_index_left = np.argmin(abs(rt_e - rt_left))  ## 找到 ±0.2min的索引
            peak_index_right = np.argmin(abs(rt_e - rt_right))
            try:
                peak_height = max(eic_e[peak_index - 2:peak_index + 2])
                other_peak = max(eic_e[peak_index - 5:peak_index + 5])
            except:
                peak_height = 1
                other_peak = 3
            rt_t, eic_t = rt_e[peak_index_left:peak_index_right], eic_e[peak_index_left:peak_index_right]
            try:
                left = argmin(abs(rt_e - (rt-0.2)))
                right = argmin(abs(rt_e -(rt+0.2)))
                rt_t1, eic_t1 = rt_e[left:right], eic_e[left:right]  ## 专门求一下左右0.2 min
                area = round(scipy.integrate.simps(eic_t1, rt_t1), 0)
            except:
                area = scipy.integrate.simps(eic_e,rt_e)
            if other_peak - peak_height > 1:
                bg_left, bg_right = 10000000, 10000000
            else:
                bg_left = cal_bg(eic_t[:int(len(eic_t) / 3)])
                bg_right = cal_bg(eic_t[-int(len(eic_t) / 3):])

            SN_left = round(peak_height / bg_left, 1)
            SN_right = round(peak_height / bg_right, 1)
            SN_all_left.append(SN_left)
            SN_all_right.append(SN_right)
            area_all.append(area)

            ### 第二步：处理质谱峰
            spec = spec_at_rt(df1, rt)
            new_spec = target_spec(spec, mz, width=0.04)

            mz_obs, error1, final_mz_opt, error2, resolution = evaluate_ms(new_spec, mz)
            mz_obs_all.append(mz_obs)
            mz_opt_all.append(final_mz_opt)
            resolution_all.append(resolution)

        final_result['SN_left'] = SN_all_left
        final_result['SN_right'] = SN_all_right
        final_result['area'] = list(map(int, area_all))
        final_result['mz'] = mz_obs_all
        final_result['intensity'] = peak_df['intensity'].values
        final_result['rt'] = peak_df['rt'].values
        final_result['resolution'] = resolution_all
        final_result['mz_opt'] = mz_opt_all
        ### 筛选条件，峰强度> i_threshold; 左边和右边SN至少一个大于SN_threshold
        final_result = final_result[(final_result['intensity'] > i_threshold) &
                                    ((final_result['SN_left'] > SN_threshold) | (
                                                final_result['SN_right'] > SN_threshold))]
        final_result = final_result.loc[:,
                       ['rt', 'mz', 'intensity', 'SN_left', 'SN_right', 'area', 'mz_opt', 'resolution']].sort_values(
            by='intensity').reset_index(drop=True)

        return final_result

    elif profile == False:
        final_result = pd.DataFrame()
        peak_num = len(peak_df['rt'])
        SN_all_left, SN_all_right, area_all = [], [], []
        for i in tqdm(range(peak_num), desc='Checking each peaks'):
            mz = peak_df.iloc[i]['mz']
            rt = peak_df.iloc[i]['rt']
            ### 第一步：处理色谱峰
            rt_e, eic_e = extract(df1, mz, error=error)
            peak_index = np.argmin(abs(rt_e - rt))  ## 找到特定时间点的索引
            rt_left = rt - 3
            rt_right = rt + 3
            peak_index_left = np.argmin(abs(rt_e - rt_left))  ## 找到 ±0.2min的索引
            peak_index_right = np.argmin(abs(rt_e - rt_right))
            try:
                peak_height = max(eic_e[peak_index - 2:peak_index + 2])
                other_peak = max(eic_e[peak_index - 5:peak_index + 5])
            except:
                peak_height = 1
                other_peak = 3
            rt_t, eic_t = rt_e[peak_index_left:peak_index_right], eic_e[peak_index_left:peak_index_right]
            try:
                area = scipy.integrate.simps(eic_e[peak_index - 40:peak_index + 40])
            except:
                area = scipy.integrate.simps(eic_e)
            if other_peak - peak_height > 1:
                bg_left, bg_right = 10000000, 10000000
            else:
                bg_left = cal_bg(eic_t[:int(len(eic_t) / 3)])
                bg_right = cal_bg(eic_t[-int(len(eic_t) / 3):])

            SN_left = round(peak_height / bg_left, 1)
            SN_right = round(peak_height / bg_right, 1)
            SN_all_left.append(SN_left)
            SN_all_right.append(SN_right)
            area_all.append(area)
        final_result['SN_left'] = SN_all_left
        final_result['SN_right'] = SN_all_right
        final_result['area'] = list(map(int, area_all))
        final_result['mz'] = peak_df['mz'].values
        final_result['intensity'] = peak_df['intensity'].values
        final_result['rt'] = peak_df['rt'].values

        ### 筛选条件，峰强度> i_threshold; 左边和右边SN至少一个大于SN_threshold
        final_result = final_result[(final_result['intensity'] > i_threshold) &
                                    ((final_result['SN_left'] > SN_threshold) | (
                                                final_result['SN_right'] > SN_threshold))]
        final_result = final_result.loc[:,
                       ['rt', 'mz', 'intensity', 'SN_left', 'SN_right', 'area']].sort_values(
            by='intensity').reset_index(drop=True)

        return final_result


def spec_at_rt(df1, rt):
    '''
    :param df1: LC-MS dataframe, genrated by the function gen_df(),or ms1 list
    :param rt:  rentention time for certain ms spec
    :return: ms spec
    '''
    if type(df1) == pd.core.frame.DataFrame:
        index = argmin(abs(df1.columns.values - rt))
        spec = df1.iloc[:, index]
    elif type(df1) == list:
        for scan in df1:
            if scan.scan_time[0]>rt:
                spec = pd.Series(data = scan.i,index = scan.mz)
                break
    return spec
        
        


def concat_alignment(files_excel):
    '''
    Concatenate all data and return
    :param files_excel: excel files
    :param mode: selected 'area' or 'intensity' for each sample
    :return: dataframe
    '''
    align = []
    data_to_concat = []
    for i in tqdm(range(len(files_excel)), desc='Finding all area files'):
        if 'area' in files_excel[i]:
            align.append(files_excel[i])
    for i in tqdm(range(len(align)), desc='Concatenating all areas'):
        name = 'data' + str(i)
        locals()[name] = pd.read_excel(align[i], index_col='Unnamed: 0')
        data_to_concat.append(locals()[name])
    final_data = pd.concat(data_to_concat, axis=1)
    return final_data


def formula_to_distribution(formula, adducts='+H', num=3):
    '''
    :param formula: molecular formula, e.g., ‘C13H13N3’
    :param adducts: ion adducts, '+H', '-H'
    :return: mz_iso, i_iso (np.array)
    '''
    f = Formula(formula)
    a = f.spectrum()
    mz_iso, i_iso = np.array([a for a in a.values()]).T
    i_iso = i_iso / i_iso[0] * 100
    if adducts == '+H':
        mz_iso += 1.00727647
    elif adducts == '-H':
        mz_iso -= 1.00727647
    mz_iso = mz_iso.round(4)
    i_iso = i_iso.round(1)
    s1 = pd.Series(data=i_iso, index=mz_iso).sort_values(ascending=False)
    return s1.index.values[:num], s1.values[:num]


def KMD_cal(mz_set, group='Br/H'):
    if '/' in group:
        g1, g2 = group.split('/')
        f1, f2 = Formula(g1), Formula(g2)
        f1, f2 = f1.spectrum(), f2.spectrum()
        f1_value, f2_value = [x for x in f1.values()][0][0], [x for x in f2.values()][0][0]
        values = [abs(f1_value - f2_value), round(abs(f1_value - f2_value), 0)]
        KM = mz_set * (max(values) / min(values))
        KMD_set = KM - np.floor(KM)

        print(f1_value, f2_value)
        print(min(values), max(values))
        print(values)
    else:
        g1 = Formula(group)
        f1 = g1.spectrum()
        f1_value = [x for x in f1.values()][0][0]
        KM = mz_set * (int(f1_value) / f1_value)
        KMD_set = KM - np.floor(mz_set)
    return KMD_set


def peak_checking_area(ref_all, df1, name):
    '''
    Based on referece pairs, extract all peaks and integrate the peak area.
    :param ref_all: all referece pairs (dataframe)
    :param df1: LC-MS dataframe, genrated by the function gen_df()
    :param name: name for area
    :return: peak_ref (dataframe)
    '''
    area_all = []
    peak_index = np.array(
        ref_all['rt'].map(lambda x: str(round(x, 2))).str.cat(ref_all['mz'].map(lambda x: str(round(x, 4))), sep='_'))
    num = len(ref_all)
    for i in tqdm(range(num)):
        rt, mz = ref_all.loc[i, ['rt', 'mz']]
        rt1, eic1 = extract(df1, mz, 50)
        rt_ind = argmin(abs(rt1 - rt))
        left = argmin(abs(rt1 - (rt - 0.2)))
        right = argmin(abs(rt1 - (rt + 0.2)))
        rt_t, eic_t = rt1[left:right], eic1[left:right]
        area = round(scipy.integrate.simps(eic_t, rt_t), 0)
        area_all.append(area)
    sample_area = pd.DataFrame(area_all, index=peak_index, columns=[name])
    return sample_area + 1


def JsonToExcel(path):
    with open(path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    Inchikey, precursor, frag, formula, smiles = [], [], [], [], []
    num = len(json_data)
    for i in range(num):
        try:
            cmp_info = json_data[i]['compound'][0]['metaData']
            Inchikey.append([x['value'] for x in cmp_info if x['name'] == 'InChIKey'][0])
            formula.append([x['value'] for x in cmp_info if x['name'] == 'molecular formula'][0])
            precursor.append([x['value'] for x in cmp_info if x['name'] == 'total exact mass'][0])
            smiles.append([x['value'] for x in cmp_info if x['name'] == 'SMILES'][0])
        except:
            Inchikey.append(None)
            formula.append(None)
            precursor.append(None)
            smiles.append(None)
        spec1 = r'{' + json_data[i]['spectrum'].replace(' ', ',') + r'}'
        spec2 = pd.Series(eval(spec1)).sort_values()
        spec3 = spec2[spec2.index[-50:]].to_dict()
        frag.append(spec3)
        print(f'\r {round(i / num * 100, 2)}%', end='')
    database = pd.DataFrame(np.array([Inchikey, precursor, frag, formula, smiles]).T,
                            columns=['Inchikey', 'Precursor', 'Frag', 'Formula', 'Smiles'])
    return database


def target_spec(spec, target_mz, width=0.04):
    '''
    :param spec: spec generated from function spec_at_rt()
    :param target_mz: target mz for inspection
    :param width: width for data points
    :return: new spec and observed mz
    '''
    index = argmin(abs(spec.index.values - target_mz))
    index_left = argmin(abs(spec.index.values - (target_mz - width)))
    index_right = argmin(abs(spec.index.values - (target_mz + width)))
    new_spec = spec.iloc[index_left:index_right]
    return new_spec

def gen_ref(files_excel, mz_error=0.015, rt_error=0.1):
    '''
    For alignment, generating a reference mz/rt pair
    :param files_excel: excel files path for extracted peaks
    :return: mz/rt pair reference
    '''
    data = []
    for i in tqdm(range(len(files_excel)),desc='Reading each excel files(gen_ref)'):
        peak1 = pd.read_excel(files_excel[i]).loc[:, ['rt', 'mz']].values
        data.append(peak1)
    print(f'\r Concatenating all peaks...                 ', end='')
    pair = np.concatenate(data, axis=0)
    peak_all_check = pair
    def align_ref(pair):
        peak_ref = []
        while len(pair) > 0:
            rt1, mz1 = pair[0]
            rt1 = round(rt1,2)
            mz1 = round(mz1,4)
            index1 = np.where((pair[:, 0] <= rt1 + rt_error) & (pair[:, 0] >= rt1 - rt_error)
                              & (pair[:, 1] <= mz1 + mz_error) & (pair[:, 1] >= mz1 - mz_error))
            peak = [rt1,mz1]
            pair = np.delete(pair, index1, axis=0)
            peak_ref.append(peak)
            print(f'\r  {len(pair)}                        ', end='')
        return peak_ref
    peak_ref = align_ref(pair)
    peak_ref0=np.array(peak_ref)
    ### 检查漏网之鱼
    pair2 = []
    for pair in tqdm(peak_all_check,desc='Second Check for gen_ref'):
        rt1,mz1 = pair
        index = np.where((peak_ref0[:, 0] <= rt1 + rt_error) & (peak_ref0[:, 0] >= rt1 - rt_error)
                                 & (peak_ref0[:, 1] <= mz1 + mz_error) & (peak_ref0[:, 1] >= mz1 - mz_error))
        if len(index[0])==0:
            pair2.append([rt1,mz1])
    peak_ref2 = align_ref(np.array(pair2))
    final_peak_ref = peak_ref+peak_ref2
    return np.array(final_peak_ref)



def ms_bg_removal(background, target_spec, i_threhold=500, mz_error=0.01):
    '''
    Only support for centroid data, please convert profile data to centroid
    :param background:  background spec
    :param target_spec:  target spec
    :param mz_error: ms widow
    :return: spec after bg removal
    '''
    target_spec = target_spec[target_spec > i_threhold]
    bg = []
    if len(target_spec) == 0:
        return None
    else:
        for i in target_spec.index.values:
            index = argmin(abs(background.index.values - i))
            if background.index.values[index] - i < mz_error:
                bg.append([i, background.values[index]])
            else:
                bg.append([i, 0])
        bg_spec = pd.Series(np.array(bg).T[1], np.array(bg).T[0], name=target_spec.name)
        spec_bg_removal = target_spec - bg_spec
        return spec_bg_removal[spec_bg_removal > i_threhold].sort_values()


def ms_to_centroid(spec):
    '''
    :param spec: profile spec ready to convert into centroid data
    :return: converted centroid data
    '''
    peaks, _ = scipy.signal.find_peaks(spec.values.copy())
    new_index = spec.index.values[peaks]
    new_values = spec.values[peaks]
    new_spec = pd.Series(new_values, new_index, name=spec.name)
    return new_spec


def spec_similarity(spec_obs, suspect_frag, error=0.005):
    '''
    :param spec_obs: observed spec
    :param suspect_frag: frag in database
    :param error: mz window
    :return:
    '''
    fragments = suspect_frag.index.values[-10:]
    score = 0
    for i in fragments:
        if min(abs(spec_obs.index.values - i)) < error:
            score += 1
    return score / len(fragments)


def evaluate_ms(new_spec, mz_exp):
    '''
    :param new_spec: target ms spec wiht width ± 0.04
    :param mz_exp:  expected mz
    :return: mz_obs, error1, final_mz_opt, error2, resolution
    '''
    peaks, _ = scipy.signal.find_peaks(new_spec.values)
    if (len(peaks) == 0) or (max(new_spec.values) < 100):
        mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    else:
        mz_obs = new_spec.index.values[peaks][argmin(abs(new_spec.index.values[peaks] - mz_exp))]
        x, y = B_spline(new_spec.index.values, new_spec.values)
        peaks, _ = scipy.signal.find_peaks(y)
        max_index = peaks[argmin(abs(x[peaks] - mz_exp))]
        half_height = y[max_index] / 2
        mz_left = x[:max_index][argmin(abs(y[:max_index] - half_height))]
        mz_right = x[max_index:][argmin(abs(y[max_index:] - half_height))]
        resolution = int(mz_obs / (mz_right - mz_left))
        mz_opt = round(mz_left + (mz_right - mz_left) / 2, 4)
        error1 = round((mz_obs - mz_exp) / mz_exp * 1000000, 1)
        error2 = round((mz_opt - mz_exp) / mz_exp * 1000000, 1)
    return mz_obs, error1, mz_opt, error2, resolution



def first_process(file, company, profile=True,ms2_analysis = True,frag_rt_error = 0.02):
    '''
    For processing HRMS data, this process will do peak picking and peak checking
    :param file: single file to process
    :param company: e.g., 'Waters', 'Agilent',etc,
    '''
    mz_round = 4
    ms1, ms2 = sep_scans(file, company)

    if company == 'Waters':
        df1 = gen_df_raw(ms1, mz_round)
        peak_all = peak_picking(df1)
        peak_selected = peak_checking(peak_all, df1, profile=profile)
    else:
        if profile == True:
            df1 = gen_df_to_centroid(ms1, mz_round)
        else:
            df1 = gen_df_raw(ms1, mz_round)
        peak_all = peak_picking(df1)
        peak_selected = peak_checking(peak_all, df1, profile=False)

    if len(ms2)==0:
        pass
    else:
        if ms2_analysis == True:
            if ('ontrol' in file)|('blank' in file)|('ethanol' in file)|('QAQC' in file)|('qaqc' in file):
                pass
            else:
                print('\n')
                print('Starting DIA ms2 analysis...')
                df2 = gen_df_raw(ms2,mz_round)
                peak_all2 = peak_picking(df2)
                peak_selected2 = peak_checking(peak_all2, df2, profile=profile)
                for i in range(len(peak_selected)):
                    rt = peak_selected.loc[i,'rt']
                    frag = str(list(peak_selected2[(peak_selected2['rt']>rt-frag_rt_error)
                                                   &(peak_selected2['rt']<rt+frag_rt_error)].sort_values(by='intensity',ascending=False)['mz'].values))
                    peak_selected.loc[i,'frag_DIA'] = frag
            
        else:
            pass
    peak_selected = identify_isotopes(peak_selected)
    peak_selected.to_excel(file.replace('.mzML', '.xlsx'))


def second_process(file, ref_all, company,profile =True):
    '''
    This process will reintegrate peak area
    :param file: single file to process
    :param ref_all: all reference peaks
    :param company: e.g., 'Waters', 'Agilent',etc,
    :return:
    '''
    mz_round = 4
    ms1, ms2 = sep_scans(file, company)
    if company == 'Waters':
        df1 = gen_df_raw(ms1, mz_round)
        
    else:
        if profile == True:
            df1 = gen_df_to_centroid(ms1, mz_round)
        else:
            df1 = gen_df_raw(ms1, mz_round)
    final_result = peak_checking_area(ref_all, df1, name=os.path.basename(file).split('.')[0])
    final_result.to_excel(file.replace('.mzML', '_final_area.xlsx'))


def extract_tic(ms1):
    '''
    For extracting TIC data
    :param ms1: ms1
    :return: rt,tic
    '''
    rt = [scan.scan_time[0] for scan in ms1]
    tic = [scan.TIC for scan in ms1]
    return rt, tic


def fold_change_filter(path, fold_change=5, area_threhold=500):
    '''
    :param path: path for all excels
    :param fold_change:  minimum fold change
    :param area_threhold: minimum area
    :return: generate unique cmps
    '''
    ### 整合blank数据，获的最大值
    print('\r Organizing blank data...         ', end='')
    excel_path = os.path.join(path, '*.xlsx')
    files_excel = glob(excel_path)
    alignment = [file for file in files_excel if 'alignment' in file]
    area_files = [file for file in files_excel if 'final_area' in file]
    blk_files = [file for file in area_files if 'blank' in file or
                 'ontrol' in file or 'QAQC' in file or 'ethanol' in file]
    blk_df = concat_alignment(blk_files)  ##生成所有blank的dataframe表
    blk_s = blk_df.max(axis=1)  ## 找到blanks中每个峰的最大值
    final_blk = blk_s.to_frame(name='blk')
    print('\r Start to process fold change         ', end='')
    ###整合每个area_file与blank的对比结果，输出fold change 大于fold_change倍的值
    area_files_sample = [file for file in area_files if 'blank' not in file and
                         'ontrol' not in file and 'QAQC' not in file and 'ethanol' not in file]
    for i in tqdm(range(len(area_files_sample)), desc='Fold change processing'):
        ###基于峰面积的对比拿到比较数据
        sample = pd.read_excel(area_files_sample[i], index_col='Unnamed: 0')
        compare = pd.concat((sample, final_blk), axis=1)
        compare['fold_change'] = (compare.iloc[:, 0] / compare.iloc[:, 1]).round(2)
        compare_result1 = compare[compare['fold_change']
                                  > fold_change].sort_values(by=compare.columns[0], ascending=False)
        compare_result = compare_result1[compare_result1[compare_result1.columns[0]] > area_threhold]
        ###开始处理alignment文件
        name = os.path.basename(area_files_sample[i]).replace('_final_area.xlsx', '')  ## 拿到名字
        alignment_path = [file for file in alignment if name in file][0]
        alignment_df = pd.read_excel(alignment_path, index_col='new_index').sort_values(by='intensity')
        alignment_df1 = alignment_df[~alignment_df.index.duplicated(keep='last')]  ## 去掉重复索引

        final_index = np.intersect1d(alignment_df1.index.values, compare_result.index.values)
        final_alignment = alignment_df1.loc[final_index, :].sort_values(by='intensity', ascending=False)
        final_alignment['fold_change'] = compare_result.loc[final_index, ['fold_change']]
        new_name = area_files_sample[i].replace('_final_area', '_unique_cmps')  ### 文件输出名称
        final_alignment.to_excel(new_name)
        
        

def classify_files(path):
    '''
    classifly the generated excel files.
    :param path: path for excel files
    :return:
    '''
    files_excel = glob(os.path.join(path, '*.xlsx'))
    step1 = os.path.join(path, 'step1_peak_picking_result')
    step2 = os.path.join(path, 'step2_peak_alignment_result')
    step3 = os.path.join(path, 'step3_all_peak_areas')
    step4 = os.path.join(path, 'step4_fold_change_filter')
    try:
        os.mkdir(step1)
    except:
        pass
    try:
        os.mkdir(step2)
    except:
        pass
    try:
        os.mkdir(step3)
    except:
        pass
    try:
        os.mkdir(step4)
    except:
        pass
    for file in files_excel:
        if 'alignment' in file:
            try:
                shutil.move(file, step2)
            except:
                pass
        elif 'final_area' in file:
            try:
                shutil.move(file, step3)
            except:
                pass
        elif 'unique_cmps' in file:
            try:
                shutil.move(file, step4)
            except:
                pass
        else:
            try:
                shutil.move(file, step1)
            except:
                pass
    files_excel = glob(os.path.join(step3, '*.xlsx'))
    all_peak_areas = concat_alignment(files_excel)
    all_peak_areas.to_excel(os.path.join(step3, 'final_result.xlsx'))


def gen_frag_DIA(ms1, ms2, rt, profile=True,i_threhold=200):
    '''
    :param ms1: ms1 list
    :param ms2: ms2 list
    :param rt: peak retention time
    :param mode:  (str) profile or centroid
    :return: frag_spec_after_bg_removal
    '''
    for ms in ms1:
        if ms.scan_time[0] > rt:
            target_ms1 = ms
            break
    for ms in ms2:
        if ms.scan_time[0] > rt:
            target_ms2 = ms
            break
    if profile == True:
        spec1 = pd.Series(data=target_ms1.i, index=target_ms1.mz)
        spec2 = pd.Series(data=target_ms2.i, index=target_ms2.mz)
        spec1 = ms_to_centroid(spec1)
        spec2 = ms_to_centroid(spec2)
        spec_bg_removal = ms_bg_removal(spec1, spec2,i_threhold=i_threhold)
    else:
        spec1 = pd.Series(data=target_ms1.i, index=target_ms1.mz)
        spec2 = pd.Series(data=target_ms2.i, index=target_ms2.mz)
        spec_bg_removal = ms_bg_removal(spec1, spec2,i_threhold=i_threhold)
    return spec_bg_removal


def ms2_search(precursor, ms2_frag, lib, mode='pos', ms2_i_threhold=2000, ms1_error=0.015, ms2_error=0.015):
    '''
    :param precursor: The measured parent compounds in LCMS
    :param ms2_frag: ms2 frag at certain retention time after background removal
    :param lib_df: library dataframe
    :param mode: 'pos' or 'neg'
    :return: result dictinary
    '''
    ms2_frag = ms2_frag[ms2_frag > ms2_i_threhold]

    if mode == 'pos':
        lib_precursor = precursor - 1.00784
    elif mode == 'neg':
        lib_precursor = precursor + 1.00784
    target_lib = lib[(lib['Precursor'] > lib_precursor - ms1_error) & (lib['Precursor'] < lib_precursor + ms1_error)]
    susp_list = list(set(target_lib['Inchikey'].values))
    precursor_floor = np.floor(lib_precursor) - 5  ## 默认碎片不太可能是mz-5

    ###定义一个接受数据的列表：
    cmp_return = {}

    ### 开始匹配
    for cmp in susp_list:
        lib_cmp = target_lib[target_lib['Inchikey'] == cmp]
        error1 = round((lib_precursor - lib_cmp['Precursor'].values[0]) / precursor * 1e6, 1)
        cmp_frags = []
        for i in range(len(lib_cmp)):
            name = 's' + str(i)
            locals()[name] = pd.Series(eval(lib_cmp['Frag'].iloc[i]))
            cmp_frags.append(locals()[name])
        cmp_frags_df = pd.concat(cmp_frags).sort_values()
        cmp_frags_df = cmp_frags_df[cmp_frags_df.index.values < precursor_floor]
        cmp_frags_df_50 = cmp_frags_df[cmp_frags_df.values > 50]
        if len(cmp_frags_df) != 0:
            if len(cmp_frags_df_50) != 0:
                dict1 = dict(Counter(cmp_frags_df_50.index.values.round(2)))
                target_frag = sorted(dict1.items(), key=lambda x: x[1])[-1][0]
                frags = np.array(cmp_frags_df_50.keys())
                final_frag = frags[(frags > target_frag - 0.015) & (frags < target_frag + 0.015)].mean()
            else:
                final_frag = cmp_frags_df.index.values[-1]

            index1 = argmin(abs(ms2_frag.index.values - final_frag))
            frag_obs = ms2_frag.index.values[index1]
            frag_obs_i = ms2_frag.values[index1]
            error2 = frag_obs - final_frag
            if abs(error2) < ms2_error:
                cmp_return[cmp] = {'mz_error': error1, 'frag_obs': round(frag_obs, 4),
                                   'frag_error': round(error2 / frag_obs * 1e6, 1), 'frag_i': frag_obs_i}
    return cmp_return


def gen_lib_result_DIA(lib_df, mzml_file, unique_excel,profile=True,mode='pos', i_min=5000, company='Waters'):
    '''
    :param lib_df:  library dataframe generated by json_to_excel function
    :param mzml_file:  DIA mzml
    :param unique_excel: unique_cmp excel files genrated after fold_change_filter function
    :param mode: 'pos' or 'neg'
    :param i_min:  minimum intensity
    :param company: 'Waters', 'Agilent',’AB‘、'Thermo'
    :return: new_unique_cmp
    '''
    print('\r Reading unique_cmp file...', end='')
    unique_df = pd.read_excel(unique_excel)
    unique_df = unique_df[unique_df['intensity'] > i_min]
    ms1, ms2 = sep_scans(mzml_file, company)
    for i in tqdm(range(len(unique_df)), desc='lib matching'):
        rt, precursor = unique_df.loc[i, ['rt', 'mz']]
        ms2_frag = gen_frag_DIA(ms1, ms2, rt, profile=profile)
        try:
            result = str(ms2_search(precursor, ms2_frag, lib_df,mode = mode))
        except:
            result = None
        unique_df.loc[i, 'matched_result'] = result
    return unique_df





def ms2_search_UNIFI(precursor, ms2_frag, lib, mode = 'pos', ms2_i_threhold=2000, ms1_error=0.015, ms2_error=0.015):
    '''
    :param precursor: The measured parent compounds in LCMS
    :param ms2_frag: ms2 frag at certain retention time after background removal
    :param lib: library dataframe, UNIFI database
    :param mode: No Need
    :return: result dictinary
    '''
    ms2_frag = ms2_frag[ms2_frag > ms2_i_threhold]
    if mode == 'pos':
        lib_df = lib
    else:
        lib_df = lib
    if len(ms2_frag)!=0:
        ### 根据precursor筛选到特定dataframe
        ms1_match_result = lib_df[lib_df['precursors'].apply(lambda x: True if min(abs(np.array(eval(x))-precursor))<ms1_error else False)]    
        cmp_return = {}  ### 定义一个字典接收数据
        for i in range(len(ms1_match_result)):
            name = ms1_match_result.iloc[i]['file_name']  ### 字典keys
            ms1_list = eval(ms1_match_result.iloc[i]['precursors'])
            ms1_exp = ms1_list[argmin(np.array(ms1_list)-precursor)]  ### 找到期待的ms1
            error1 = round((precursor-ms1_exp)/precursor*1e6,1)
            ms2_list = eval(ms1_match_result.iloc[i]['CIDs'])  ###拿到ms2 list
            dict1_all = []
            for mz in ms2_list:
                dict1 = {}
                min_index = argmin(abs(ms2_frag.index.values-mz))
                if ms2_frag.index.values[min_index]-mz <ms2_error:
                    dict1['frag'] = ms2_frag.index.values[min_index]
                    dict1['error2'] = round((ms2_frag.index.values[min_index]-mz)/mz*1e6,1)
                    dict1['frag_intensity'] = ms2_frag.values[min_index]
                    dict1_all.append(dict1)
            dict2 = dict(pd.DataFrame(dict1_all).sort_values(by = 'intensity').iloc[-1])
            dict2['error1'] = error1
            ###把dict2负值给外部字典
            cmp_return[name] = dict2
    else:
        cmp_return = {}
    return cmp_return



def identify_isotopes(cmp,iso_error = 0.005):
    '''
    :param cmp: unique compounds dataframe
    :return: unique compounds dataframe with isotope peak labeled
    '''
    ###元素周期表
    atom_mass_table = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,'Cliso':36.965903,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336,'Briso':80.916290, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })

    ### 计算不同同位素和adducts之间的差值
    Ciso = atom_mass_table['Ciso'] - atom_mass_table['C']
    Siso = atom_mass_table['Siso'] - atom_mass_table['S']
    Cliso = atom_mass_table['Cliso'] - atom_mass_table['Cl']
    Briso = atom_mass_table['Briso'] - atom_mass_table['Br']
    SClBr_iso = np.mean([Siso,Cliso,Briso])
    Na = atom_mass_table['Na'] - atom_mass_table['H']
    K = atom_mass_table['K'] - atom_mass_table['H']
    NH3 = 3*atom_mass_table['H'] + atom_mass_table['N']
    H2O = 2*atom_mass_table['H'] + atom_mass_table['O']
    
    all_rts = list(set(cmp['rt'].values))
    for i in tqdm(range(len(all_rts))):
        cmp_rt = cmp[(cmp['rt'] >= all_rts[i]-0.015)&(cmp['rt'] <= all_rts[i]+0.015)].sort_values(by='mz')
        mzs = cmp_rt['mz'].values
        for mz in mzs:
            C_fold = 1
            differ = mzs - mz
            ###拿到此mz的intensity
            mz_i = cmp_rt[cmp_rt['mz'] == mz]['intensity'].values[0] ## 数值
            
            ## 搜索C13同位素
            i_C13_1 = np.where((differ < Ciso+iso_error) & (differ > Ciso-iso_error))[0]
            if len(i_C13_1) == 0:
                pass
            elif len(i_C13_1) == 1:
                index_ = cmp_rt.index[i_C13_1]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if  mz_i * C_fold > compare_i:
                    cmp.loc[index_, 'Ciso'] = f'C13:{all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_C13_1]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if mz_i * C_fold > compare_i:
                        cmp.loc[index, 'Ciso'] = f'C13: {all_rts[i]} _{mz}'
                    
            ## 搜索Cl同位素
            i_Cl = np.where((differ < Cliso+iso_error) & (differ > Cliso-iso_error))[0]
            if len(i_Cl) == 0:
                pass
            elif len(i_Cl) == 1:
                index_ = cmp_rt.index[i_Cl]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if (mz_i *0.45 > compare_i)&(mz_i *0.2 < compare_i):
                    cmp.loc[index_, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                elif (mz_i *0.5 < compare_i)&(mz_i *0.8 > compare_i):
                    cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                elif (mz_i *0.8 < compare_i)&(mz_i *1.2 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                elif (mz_i *1.5 < compare_i)&(mz_i *2.5 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'

            else:
                index_ = cmp_rt.index[i_Cl]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if (mz_i *0.45 > compare_i)&(mz_i *0.2 < compare_i):
                        cmp.loc[index, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                    elif (mz_i *0.5 < compare_i)&(mz_i *0.8 < compare_i):
                        cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                    elif (mz_i *0.8 < compare_i)&(mz_i *1.2 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                    elif (mz_i *1.5 < compare_i)&(mz_i *2.5 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'
            
            
            ## 搜索+Na+峰
            i_Na = np.where((differ < Na+iso_error) & (differ > Na-iso_error))[0] ## Na+:22.9892, Na+-H: 21.9814
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'

            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'
            
            ## 搜索+K+峰
            i_Na = np.where((differ < K+iso_error) & (differ > K-iso_error))[0] 
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'
                
            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'    
                    
           ### 搜索+NH4+峰
            i_NH4 = np.where((differ < NH3+iso_error) & (differ > NH3-iso_error))[0] #NH3:17.0266
            if len(i_NH4) == 0:
                pass
            elif len(i_NH4) == 1:
                index_ = cmp_rt.index[i_NH4]
                cmp.loc[index_, 'NH4 adducts'] = f'NH4 adducts:  {all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_NH4]
                for index in index_:
                    cmp.loc[index, 'NH4 adducts'] = f'NH4 adducts: {all_rts[i]} _{mz}'
            
    return cmp



def database_quantification(mzml_files,local_database):
    '''
    To integrate peaks and return areas for quantification based on local_database
    :param mzml_files: mzml files
    :param local_database: local database dataframe
    :return: dataframe
    '''
    for file in mzml_files:
        name = os.path.basename(file).replace('.mzML','')
        ms1,ms2 = sep_scans(file,'Waters')
        df1 = gen_df_raw(ms1)
        for i in range(len(local_database)):
            mz,rt = local_database.loc[i,['mz_exp','rt']]
            rt1, eic1 = extract(df1, mz, 50)
            rt_ind = argmin(abs(rt1 - rt))
            left = argmin(abs(rt1 - (rt - 0.2)))
            right = argmin(abs(rt1 - (rt + 0.2)))
            rt_t, eic_t = rt1[left:right], eic1[left:right]
            area = round(scipy.integrate.simps(eic_t, rt_t), 0)
            local_database.loc[i,f'{name}'] = area
    return local_database


def append_list(mz,loop_num, atoms, atom_n):
    '''
    For formula prediction function
    
    '''
    pattern = []
    if loop_num == 2:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            for j in range(atom_n[1][0], atom_n[1][1] + 2):
                pattern.append([i, j])
    if loop_num == 3:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            for j in range(atom_n[1][0], atom_n[1][1] + 2):
                for k in range(atom_n[2][0], atom_n[2][1] + 2):
                    pattern.append([i, j, k])
    if loop_num == 4:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]]*i  ### i还剩多少质量
            j1 = int(np.floor(i_mz_remain/atom_mass_table[atoms[1]])) if int(np.floor(i_mz_remain/atom_mass_table[atoms[1]]))< atom_n[1][1] else  atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                for k in range(atom_n[2][0], atom_n[2][1] + 2):
                    for l in range(atom_n[3][0], atom_n[3][1] + 2):
                        pattern.append([i, j, k, l])
        ###五个原子
    if loop_num == 5:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]]*i  ### i还剩多少质量
            j1 = int(np.floor(i_mz_remain/atom_mass_table[atoms[1]])) if int(np.floor(i_mz_remain/atom_mass_table[atoms[1]]))< atom_n[1][1] else  atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j ### j还剩多少质量
                k1 = int(np.floor(j_mz_remain/atom_mass_table[atoms[2]])) if int(np.floor(j_mz_remain/atom_mass_table[atoms[2]]))< atom_n[2][1] else  atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    for l in range(atom_n[3][0], atom_n[3][1] + 2):
                        for m in range(atom_n[4][0], atom_n[4][1] + 2):
                            pattern.append([i, j, k, l, m])
        ###六个原子
    if loop_num == 6:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]]*i  ### i还剩多少质量
            j1 = int(np.floor(i_mz_remain/atom_mass_table[atoms[1]])) if int(np.floor(i_mz_remain/atom_mass_table[atoms[1]]))< atom_n[1][1] else  atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j ### j还剩多少质量
                k1 = int(np.floor(j_mz_remain/atom_mass_table[atoms[2]])) if int(np.floor(j_mz_remain/atom_mass_table[atoms[2]]))< atom_n[2][1] else  atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    k_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j -atom_mass_table[atoms[2]]*k ### k还剩多少质量
                    l1 = int(np.floor(k_mz_remain/atom_mass_table[atoms[3]])) if int(np.floor(k_mz_remain/atom_mass_table[atoms[3]]))< atom_n[3][1] else  atom_n[3][1]
                    for l in range(atom_n[3][0], l1 + 2):
                        for m in range(atom_n[4][0], atom_n[4][1] + 2):
                            for n in range(atom_n[5][0], atom_n[5][1] + 2):
                                pattern.append([i, j, k, l, m,n])
    ###七个原子
    if loop_num == 7:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]]*i  ### i还剩多少质量
            j1 = int(np.floor(i_mz_remain/atom_mass_table[atoms[1]])) if int(np.floor(i_mz_remain/atom_mass_table[atoms[1]]))< atom_n[1][1] else  atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j ### j还剩多少质量
                k1 = int(np.floor(j_mz_remain/atom_mass_table[atoms[2]])) if int(np.floor(j_mz_remain/atom_mass_table[atoms[2]]))< atom_n[2][1] else  atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    k_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j -atom_mass_table[atoms[2]]*k ### k还剩多少质量
                    l1 = int(np.floor(k_mz_remain/atom_mass_table[atoms[3]])) if int(np.floor(k_mz_remain/atom_mass_table[atoms[3]]))< atom_n[3][1] else  atom_n[3][1]
                    for l in range(atom_n[3][0], l1 + 2):
                        l_mz_remain = mz - atom_mass_table[atoms[0]]*i -atom_mass_table[atoms[1]]*j -atom_mass_table[atoms[2]]*k -atom_mass_table[atoms[3]]*l ### l还剩多少质量
                        m1 = int(np.floor(l_mz_remain/atom_mass_table[atoms[4]])) if int(np.floor(l_mz_remain/atom_mass_table[atoms[4]]))< atom_n[4][1] else  atom_n[4][1]
                        for m in range(atom_n[4][0], m1 + 2):
                            for n in range(atom_n[5][0], atom_n[5][1] + 2):
                                for o in range(atom_n[6][0], atom_n[6][1] + 2):
                                    pattern.append([i, j, k, l, m,n,o])


    return pattern




def formula_prediction(mz, error=500, atoms1=[], atom_n1=[], mode='pos'):
    '''
    To predict the possible formula based on mass and possible atoms,support 7 atoms max.
    :param mz: mz to predict
    :param error: mass error tolerance
    :param atoms:  atoms for prediction, e.g.,['C','H','O','N']
    :param atom_n: atoms number range, e.g., [[0,15],[0,20],[0,10],[0,10]]
    :param mode: 'pos' or 'neg'
    :return: prediction result
    '''
    atoms=copy.deepcopy(atoms1)
    atom_n=copy.deepcopy(atom_n1)
    atom_mass_table = pd.Series(data={'C': 12.000000, 'N': 14.003074, 'O': 15.994915, 'H': 1.007825,
                                      'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
                                      'S': 31.972072, 'Br': 78.918336, 'Na': 22.989770,'Si':27.976928,
                                     'Fe':55.934939,'Se':79.916521,'As':74.921596,'I':126.904477,'D':2.014102,
                                     'Co':58.933198,'Au':196.966560,'B':11.009305,
                                     })
    
    ### 纠错机制,把明显不可能的删除掉，提高效率
    for i in range(len(atoms)):
        num = int(np.floor(mz/atom_mass_table[atoms[i]])) if int(np.floor(mz/atom_mass_table[atoms[i]]))<atom_n[i][1] else atom_n[i][1]
        atom_n[i][1]=num
    
    
    ### 矫正formula
    def process_formula(formula):
        b = re.findall('[A-Z][a-z]*|\d+',formula)
        c=''
        for i in range(len(b)):
            if b[i].isdigit():
                if eval(b[i])==1:
                    c += b[i-1]
                elif eval(b[i])>1:
                    c += b[i-1]
                    c += b[i]
        return c
    
    
    
    mz_h = mz * (1 + error * 1e-6)
    mz_l = mz * (1 - error * 1e-6)
    a = len(atoms)
    b = len(atom_n)
    pattern = []
    
    if (a > 0) & (a == b):
        pattern = append_list(mz,a, atoms, atom_n)

    else:
        if a <= 0:
            print('Atoms number is 0')
        else:
            print(f'There are {a} atoms,but numbers only have {b}')

    p_df = pd.DataFrame(pattern, columns=atoms)
    
    data_all = []
    for atom in p_df.columns:
        data_all.append(p_df[atom] * atom_mass_table[atom])
    df_ = pd.concat(data_all, axis=1)
    if mode == 'pos':
        p_df['mass'] = df_.sum(axis=1).values - 0.000549
    else:
        p_df['mass'] = df_.sum(axis=1).values + 0.000549
    
    p_df['error'] = ((p_df['mass'].values - mz) / mz * 1e6).round(1)
    p_df['error_abs'] = abs(((p_df['mass'].values - mz) / mz * 1e6).round(1))
    

    
    p_df = p_df[(p_df['mass'] >= mz_l) & (p_df['mass'] <= mz_h)].sort_values(by='error_abs').reset_index(drop=True)

    ## 转成formula
    
    formula1 = p_df.columns[0]+p_df.iloc[:,0].astype(str)
    for i in range(1,a):                
        formula1+= p_df.columns[i]+p_df.iloc[:,i].astype(str)
    p_df['formula'] = formula1.apply(process_formula)
    ###############
    
    return p_df.loc[:,['formula','mass','error']]




def formula_sep(formula):
    '''
    Transform formula to atoms list and atoms number list.
    :param formula: 
    '''
    a = re.findall('[A-Z][a-z]*|\d+',formula)
    b = {}
    for i in range(len(a)):
        try:
            eval(a[i])
        except:
            try:  
                b[a[i]]=eval(a[i+1])
            except:
                b[a[i]]=1
    c = pd.Series(b)
    atoms = list(c.index)
    atom_n1 = list(c.values)
    atom_n = []
    for num in atom_n1:
        atom_n.append([0,num])
    return atoms,atom_n

def frag_correction(mz,formula,mode):
    '''
    Correct the observed mz to theoretical mz.
    :param mz: observed mz
    :param formula: precursor formula or atom range
    :param mode: 'pos' or 'neg'
    :return: frag_formula, mz_opt, error
    '''
    atoms,atom_n = formula_sep(formula)
    result = formula_prediction(mz,50,atoms,atom_n,mode=mode)
    if len(result)==0:
        frag_formula, mass, error = None, None, None
    else:
        frag_formula, mass, error = result.loc[0,['formula','mass','error']]
    return frag_formula, mass, error




def FT_ICRMS(path, formula='C50H60O50N1S1', mz_range=[200, 800], peak_threshold=6, error=1, iso_error=0.0003,
             iso_fold_change=2,mode = 'neg'):
    '''
    :param path: file path, support for profile raw data, format: .xy, .csv, .xlsx
    :param formula: formula range for prediction
    :param mz_range: mz range for prediction
    :param peak_threshold: Similar to signal to noise.
    :param error: mz error for formula prediction, unit: part per million(ppm)
    :param iso_error: mz error for isotope assignment, unit: Dalton
    :param iso_fold_change: the peak intensit/isotope intensity
    :return: A dataframe with formula prediction
    '''
    atom_mass_table = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })

    #######查找同位素的函数
    def find_isotopes(data, atom_mass_table, error=0.0003, iso_fold_change=5):

        Ciso = atom_mass_table['Ciso'] - atom_mass_table['C']
        Niso = atom_mass_table['Niso'] - atom_mass_table['N']
        Oiso = atom_mass_table['Oiso'] - atom_mass_table['O']
        Siso = atom_mass_table['Siso'] - atom_mass_table['S']
        Ciso_all = []
        Niso_all = []
        Oiso_all = []
        Siso_all = []

        for mz in tqdm(data['m/z'].values, desc='Finding isotopes'):
            mz_i = data[data['m/z'] == mz]['i'].values[0]
            mz_s = data['m/z'] - mz
            C = np.where((mz_s < Ciso + error) & (mz_s > Ciso - error))
            C_i = data.loc[C[0]]['i']
            N = np.where((mz_s < Niso + error) & (mz_s > Niso - error))
            N_i = data.loc[N[0]]['i']
            O = np.where((mz_s < Oiso + error) & (mz_s > Oiso - error))
            O_i = data.loc[O[0]]['i']
            S = np.where((mz_s < Siso + error) & (mz_s > Siso - error))
            S_i = data.loc[S[0]]['i']

            if len(C[0]) > 0:
                if mz_i > iso_fold_change * C_i.values[0]:
                    Ciso_all.append(int(C[0]))
            if len(N[0]) > 0:
                if mz_i > iso_fold_change * N_i.values[0]:
                    Niso_all.append(int(N[0]))
            if len(O[0]) > 0:
                if mz_i > iso_fold_change * O_i.values[0]:
                    Oiso_all.append(int(O[0]))
            if len(S[0]) > 0:
                if mz_i > iso_fold_change * S_i.values[0]:
                    Siso_all.append(int(S[0]))
        return np.array(Ciso_all), np.array(Niso_all), np.array(Oiso_all), np.array(Siso_all)

    #######生成所有可能的formula
    def generate_formula_df(mz_range, atoms, atom_n,mode=mode):
        '''
        generate possible formula set for mz range
        '''
        if mode == 'pos':
            e = -atom_mass_table['e']
        elif mode == 'neg':
            e = atom_mass_table['e']
        
        pattern = []
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]] * i  ### i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table[atoms[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table[atoms[1]])) < atom_n[1][1] else atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j  ### j还剩多少质量
                k1 = int(np.floor(j_mz_remain / atom_mass_table[atoms[2]])) if int(
                    np.floor(j_mz_remain / atom_mass_table[atoms[2]])) < atom_n[2][1] else atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    for l in range(atom_n[3][0], atom_n[3][1] + 2):
                        for m in range(atom_n[4][0], atom_n[4][1] + 2):
                            pattern.append([i, j, k, l, m])
        pattern_df = pd.DataFrame(pattern, columns=atoms)
        pattern_df['m/z_exp'] = (pattern_df[atoms[0]] * atom_mass_table[atoms[0]] +
                                 pattern_df[atoms[1]] * atom_mass_table[atoms[1]] +
                                 pattern_df[atoms[2]] * atom_mass_table[atoms[2]] +
                                 pattern_df[atoms[3]] * atom_mass_table[atoms[3]] +
                                 pattern_df[atoms[4]] * atom_mass_table[atoms[4]] + e)
        pattern_df = pattern_df.sort_values(by='m/z_exp')
        pattern_df = pattern_df[
            (pattern_df['m/z_exp'] > mz_range[0]) & (pattern_df['m/z_exp'] < mz_range[1]) & (pattern_df['C'] >= 3) & (
                        pattern_df['H'] >= 1) & (pattern_df['O'] >= 1)].reset_index(drop=True)
        return pattern_df

    #######开始匹配
    def formula_match(data, pattern_df, error=1.05, iso_error=0.0003, iso_fold_change=5):
        ###匹配同位素
        def iso_match(data, Ciso_index, pattern_df, marker, error=1.05):
            final_data = []
            for i in tqdm(range(len(data.loc[Ciso_index])), desc=f'matching {marker} isotope'):
                iso = marker[0] + 'iso'
                mz = data.loc[Ciso_index].iloc[i, 0] - atom_mass_table[iso]
                df2 = pattern_df[(pattern_df['m/z_exp'] < mz * (1 + error * 1e-6)) & (
                            pattern_df['m/z_exp'] > mz * (1 - error * 1e-6))].copy()
                df2 = df2[(df2['C']>=df2['O']/1.2)&(df2['C']>=df2['H']/2.5)]  ###筛选条件
                if len(df2) == 0:
                    pass
                else:
                    df2['m/z_obs'] = data.loc[Ciso_index].iloc[i, 0]
                    df2['intensity'] = data.loc[Ciso_index].iloc[i, 1]
                    df2['error(ppm)'] = ((df2['m/z_exp'] - mz) / mz * 1 * 1e6).round(4)
                    df2['error_abs'] = df2['error(ppm)'].abs()
                    df2['hetero'] = df2['N'] + df2['S']
                    df2['isotope'] = marker
                    s1 = df2.sort_values(by='hetero').iloc[0]
                    s1.loc[marker[0]] += 1
                    s1.loc['m/z_exp'] += atom_mass_table[iso]
                    final_data.append(s1)
            if len(final_data)==0:
                return None
            else:
                return pd.concat(final_data, axis=1).T

        ### 匹配普通峰
        def normal_match(data, Ciso_index, pattern_df, marker, error=1.05):
            final_data = []
            for i in tqdm(range(len(data.loc[Ciso_index])), desc='matching normal peaks'):
                mz = data.loc[Ciso_index].iloc[i, 0]
                df2 = pattern_df[(pattern_df['m/z_exp'] < mz * (1 + error * 1e-6)) & (
                            pattern_df['m/z_exp'] > mz * (1 - error * 1e-6))].copy()
                df2 = df2[(df2['C']>=df2['O']/1.2)&(df2['C']>=df2['H']/2.5)]  ###筛选条件
                if len(df2) == 0:
                    pass
                else:
                    df2['m/z_obs'] = mz
                    df2['intensity'] = data.loc[Ciso_index].iloc[i, 1]
                    df2['error(ppm)'] = ((df2['m/z_exp'] - mz) / mz * 1 * 1e6).round(4)
                    df2['error_abs'] = df2['error(ppm)'].abs()
                    df2['hetero'] = df2['N'] + df2['S']
                    df2['isotope'] = marker
                    s1 = df2.sort_values(by='hetero').iloc[0]
                    final_data.append(s1)
            if len(final_data)==0:
                return None
            else:
                return pd.concat(final_data, axis=1).T

        # 开始处理
        Ciso_index, Niso_index, Oiso_index, Siso_index = find_isotopes(data, atom_mass_table, iso_error,
                                                                       iso_fold_change)

        all_iso_index = np.concatenate([Ciso_index, Niso_index, Oiso_index, Siso_index])
        peak_no_iso = np.delete(data.index.values, all_iso_index.astype(int))
        ### 处理同位素
        data_to_concat = []
        if len(Ciso_index) != 0:
            Ciso_df = iso_match(data, Ciso_index, pattern_df, 'C13', error=error)
            data_to_concat.append(Ciso_df)
        if len(Niso_index) != 0:
            Niso_df = iso_match(data, Niso_index, pattern_df, 'N15', error=error)
            data_to_concat.append(Niso_df)
        if len(Oiso_index) != 0:
            Oiso_df = iso_match(data, Oiso_index, pattern_df, 'O18', error=error)
            data_to_concat.append(Oiso_df)
        if len(Siso_index) != 0:
            Siso_df = iso_match(data, Siso_index, pattern_df, 'S34', error=error)
            data_to_concat.append(Siso_df)
        ## 处理其他
        peak_no_iso_df = normal_match(data, peak_no_iso, pattern_df, '', error=error)
        data_to_concat.append(peak_no_iso_df)

        return pd.concat(data_to_concat)

    ###读取数据
    raw_data = pd.read_csv(path, delimiter=' ', names=['m/z', 'i'])

    ##分割分子式
    atoms, atom_n = formula_sep(formula)
    mz = mz_range[1]
    for i in range(len(atoms)):
        num = int(np.floor(mz / atom_mass_table[atoms[i]])) if int(np.floor(mz / atom_mass_table[atoms[i]])) < \
                                                               atom_n[i][1] else atom_n[i][1]
        atom_n[i][1] = num

    ###找到峰
    eic = raw_data.loc[:, 'i']
    index, index_left, index_right = peak_finding(eic, threshold=peak_threshold)
    data = raw_data.loc[index, :].reset_index(drop=True)
    background = np.mean(eic)*2.5
    ###生成所有可能的formula
    pattern_df = generate_formula_df(mz_range, atoms, atom_n)

    ###开始匹配
    final_result = formula_match(data, pattern_df, error=error, iso_error=iso_error, iso_fold_change=iso_fold_change)
    final_result = final_result.sort_values(by='m/z_obs').reset_index(drop=True)
    
    ### 矫正formula,把C13H13O3N0S0转成C13H13N3
    def process_formula(formula,mode):
        b = re.findall('[A-Z][a-z]*|\d+', formula)
        for j in range(len(b)):
            if (b[j] =='H')&(mode =='pos'):
                b[j+1]=str(eval(b[j+1])-1)
            elif (b[j] =='H')&(mode =='neg'):
                b[j+1]=str(eval(b[j+1])+1)
        c = ''
        for i in range(len(b)):
            if b[i].isdigit():
                if eval(b[i]) == 1:
                    c += b[i - 1]
                elif eval(b[i]) > 1:
                    c += b[i - 1]
                    c += b[i]
        return c
    
    ### 把所有formula整合
    formula1 = final_result.columns[0] + final_result.iloc[:, 0].astype(str)
    for i in range(1, 5):
        formula1 += final_result.columns[i] + final_result.iloc[:, i].astype(str)
    final_result['formula'] = formula1.apply(process_formula,mode=mode)
    
    #### 计算其他参数
    final_result['S/N'] = (final_result['intensity']/background).astype(float).round(2)
    final_result['O/C'] = (final_result['O']/final_result['C']).astype(float).round(3)

    if mode == 'pos':
        x = 1
    elif mode == 'neg':
        x = -1
    final_result['H/C'] = ((final_result['H']-x)/final_result['C']).astype(float).round(3)
    final_result['DBE'] = 1+0.5*(2*final_result['C']- (final_result['H']-x)+final_result['N'])
    final_result['NOSC'] = 4 - (4*final_result['C']+(final_result['H']-x)
                                -3*final_result['N']-2*final_result['O']-2*final_result['S'])/final_result['C']
    final_result['NOSC']=final_result['NOSC'].astype(float).round(3)
    AI_denominator = final_result['C']-0.5*final_result['O']-final_result['S']-final_result['N']
    AI_numerator = 1 +final_result['C']-0.5*final_result['O']-final_result['S']-0.5*(final_result['H']-x)
    AI = AI_numerator/(AI_denominator.sort_values()+1*1e-6)
    final_result['AI'] = AI
    return final_result


def concat_list(l):
    '''
    Finding list with same elements and concat them into one list
    :param l: list to concat
    :return: final list
    '''
    G = nx.Graph()
    #将节点添加到Graph    
    G.add_nodes_from(sum(l, []))
    #从节点列表创建边
    q = [[(s[i],s[i+1]) for i in range(len(s)-1)] for s in l]
    for i in q:
        #向Graph添加边
        G.add_edges_from(i)
    #查找每个组件的图形和列表节点中的所有连接组件
    final_list = [list(i) for i in nx.connected_components(G)]
    return final_list



def gen_possible_formula(formula,mz_range=[50,1000],mode='pos'):
    mz = mz_range[1]
    atoms,atom_n = formula_sep(formula)
    ## 删除不可能的组合
    for i in range(len(atoms)):
        num = int(np.floor(mz/atom_mass_table[atoms[i]])) if int(np.floor(mz/atom_mass_table[atoms[i]]))<atom_n[i][1] else atom_n[i][1]
        atom_n[i][1]=num
    ###  开始匹配
    pattern_df = pd.DataFrame(append_list(mz,len(atoms),atoms, atom_n),columns = atoms)
    pattern_df = pattern_df[(pattern_df['C']>2)&(pattern_df['H']>2)&(pattern_df['C']>=pattern_df['O']/1.2)&(pattern_df['C']>=pattern_df['H']/2.5)]
    
    a = pattern_df[atoms[0]] * atom_mass_table[atoms[0]]
    for i in range(len(atoms)-1):
        a += pattern_df[atoms[i+1]] * atom_mass_table[atoms[i+1]]
    if mode =='pos':
        pattern_df['m/z_exp'] = a-0.0005
    elif mode == 'neg':
        pattern_df['m/z_exp'] = a+0.0005
    return pattern_df[pattern_df['m/z_exp']<mz_range[1]].reset_index(drop=True)



def gen_DDA_ms2_df(path,profile = True):
    '''
    :param path: DDA mzml file path 
    :return: DataFrame with rt, precursor and fragments info
    '''
    ms1,ms2 = sep_scans(path,'Waters')
    precursors,rts,frags = [],[],[]
    for scan in ms2:
        precursor = scan.selected_precursors[0]['mz']
        precursors.append(precursor)
        rt = round(scan.scan_time[0],3)
        rts.append(rt)
        mz = scan.mz
        intensity = scan.i
        if profile ==True:
            spec = pd.Series(data = intensity,index = mz)
            new_spec = ms_to_centroid(spec)
            mz = new_spec.index.values
            intensity = new_spec.values
        else:
            pass
        
        s = pd.Series(data = intensity,index=mz).sort_values(ascending=False).iloc[:20]
        frag = [list(s.index.values.round(4)),list(s.values)]
        frags.append(frag)
    DDA_df= pd.DataFrame([precursors,rts,frags],index=['precursor','rt','frag']).T
    return DDA_df


def one_step_process(path,company,profile=True, ms2_analysis = True, fold_change=5, area_threhold=500):
    '''
    For beginers, one step process will greatly simplify this process.
    :param path: path for mzml files
    :param company: company for LC-HRMS data
    :param profile: False or True
    :param fold_change: False or a number
    :param area_threhold: area threhold
    '''
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    mz_round =4
    
    for file in files_mzml:
        ms1, ms2 = sep_scans(file, company)
        if company == 'Waters':
            df1 = gen_df_raw(ms1, mz_round)
            peak_all = peak_picking(df1)
            peak_selected = peak_checking(peak_all, df1, profile=profile)
            peak_selected = identify_isotopes(peak_selected)
        else:
            if profile == False:
                df1 = gen_df_raw(ms1,mz_round)
            else:
                df1 = gen_df_to_centroid(ms1,mz_round)
            peak_all = peak_picking(df1)
            peak_selected = peak_checking(peak_all, df1, profile=False)
            peak_selected = identify_isotopes(peak_selected)
        peak_selected.to_excel(file.replace('.mzML', '.xlsx'))
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    for file in files_mzml:
        ms1, *_ = sep_scans(file, company)
        if company == 'Waters':
            df1 = gen_df_raw(ms1, mz_round)
            peak_all = peak_picking(df1)
            peak_selected = peak_checking(peak_all, df1, profile=profile)
        else:
            if profile == False:
                df1 = gen_df_raw(ms1,mz_round)
            else:
                df1 = gen_df_to_centroid(ms1,mz_round)       
        final_result = peak_checking_area(ref_all, df1, name=os.path.basename(file).split('.')[0])
        final_result.to_excel(file.replace('.mzML', '_final_area.xlsx'))
    ### 处理fold_change
    if fold_change == False:
        pass
    else:
        fold_change_filter(path, fold_change=fold_change, area_threhold=area_threhold)
        files_excel = glob(os.path.join(path, '*.xlsx'))
        classify_files(path)

        

def compare_frag(frag_obs,frag_exp,error=0.015):
    '''
    compare lists
    '''
    compare_result = {}
    if len(frag_obs)<len(frag_exp):
        for mz in frag_obs:
            index = argmin(abs(frag_exp-mz))
            matched_mz = frag_exp[index]
            compare_result[mz]=matched_mz-mz
    else:
        for mz in frag_exp:
            index = argmin(abs(frag_obs-mz))
            matched_mz = frag_obs[index]
            compare_result[matched_mz]=mz-matched_mz
    if len(compare_result)==0:
        s2 = []
    else:
        s1 = pd.Series(compare_result)
        s2 = s1[s1.abs()<error]
    return s2

def ms2_matching(unique,database,ms1_error = 50, ms2_error = 0.015):
    '''
    unique excel file must have column with name 'mz','frag_DIA'
    '''

    columns = list(unique.columns.values)
    
    DIA = [column for column in columns if 'DIA' in column]
    DDA = [column for column in columns if 'DDA' in column]

    if len(DIA)!=0:
        for i in tqdm(range(len(unique))):
            mz = unique.loc[i]['mz']
            precursor = mz - 1.0078
            frag_obs = np.array(eval(unique.loc[i][DIA[0]]))

            ### 根据 precursor在数据库database里做ms1匹配
            match_result = database[(database['Precursor']<precursor*(1+ms1_error*1e-6))&(database['Precursor']>precursor*(1-ms1_error*1e-6))]

            match_result_dict = []  ### 定义一个列表接收数据
            ### 对匹配结果依次分析
            if len(match_result)==0:   ### 匹配失败
                pass
            else:
                for j in range(len(match_result)):     
                    ik_match = match_result['Inchikey'].iloc[j] ### 匹配的ik
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match-precursor)/precursor*1e6,1) ### 计算ms1 error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                    except:
                        frag_exp = []

                    compare_result = compare_frag(frag_obs,frag_exp,error=0.015)
                    if len(compare_result)==0:
                        pass
                    else:
                        single_result_dict = {}   ### 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  #匹配的具体数据
                        match_num = len(compare_frag_dict)                 #匹配的个数

                        match_percent = round(len(compare_frag_dict)/len(set(frag_exp.round())),2) #匹配的百分比

                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        match_result_dict.append(single_result_dict)
            ### 输出结果
            unique.loc[i,'match_result_DIA'] = str(match_result_dict)
            ##
            if len(match_result_dict)==0:
                pass
            else:
                optmized_result = pd.concat([pd.Series(a) for a in match_result_dict],axis=1).T.sort_values(by = ['match_num','ms1_error','match_percent'],ascending=[False,True,False])
                unique.loc[i,'best_results_DIA'] = optmized_result['ik'].iloc[0]
    
    if len(DDA)!=0:
        for i in tqdm(range(len(unique))):
            mz = unique.loc[i]['mz']
            precursor = mz - 1.0078
            frag_obs = np.array(eval(unique.loc[i][DDA[0]]))

            ### 根据 precursor在数据库database里做ms1匹配
            match_result = database[(database['Precursor']<precursor*(1+ms1_error*1e-6))&(database['Precursor']>precursor*(1-ms1_error*1e-6))]

            match_result_dict = []  ### 定义一个列表接收数据
            ### 对匹配结果依次分析
            if len(match_result)==0:   ### 匹配失败
                pass
            else:
                for j in range(len(match_result)):     
                    ik_match = match_result['Inchikey'].iloc[j] ### 匹配的ik
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match-precursor)/precursor*1e6,1) ### 计算ms1 error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                    except:
                        frag_exp = []

                    compare_result = compare_frag(frag_obs,frag_exp,error=0.015)
                    if len(compare_result)==0:
                        pass
                    else:
                        single_result_dict = {}   ### 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  #匹配的具体数据
                        match_num = len(compare_frag_dict)                 #匹配的个数

                        match_percent = round(len(compare_frag_dict)/len(set(frag_exp.round())),2) #匹配的百分比

                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        match_result_dict.append(single_result_dict)
            ### 输出结果
            unique.loc[i,'match_result_DDA'] = str(match_result_dict)
            ##
            if len(match_result_dict)==0:
                pass
            else:
                optmized_result = pd.concat([pd.Series(a) for a in match_result_dict],axis=1).T.sort_values(by = ['match_num','ms1_error','match_percent'],ascending=[False,True,False])
                unique.loc[i,'best_results_DDA'] = optmized_result['ik'].iloc[0]
        
    return unique


def multi_process(path,company,profile = True, processors=5,ms2_analysis=True,fold_change = 5,area_threhold = 200):
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml_DDA = [file for file in files_mzml if 'DDA' in os.path.basename(file)]
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    ### 第一个过程
    pool = Pool(processes=processors)
    for file in files_mzml:
        print(file)
        pool.apply_async(first_process, args=(file, company,profile,ms2_analysis))
    print('First process started...')
    pool.close()
    pool.join()

    ### 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')

    ### 第二个过程
    pool = Pool(processes=processors)
    for file in files_mzml:
        print(file)
        pool.apply_async(second_process, args=(file, ref_all, company,profile))
    print('Second process started...')
    pool.close()
    pool.join()
    
    ### 第三个过程, 做fold change filter
    fold_change_filter(path,fold_change =fold_change,area_threhold = area_threhold)
    
    ### 如果有DDA，分析DDA
    files_excel = glob(os.path.join(path, '*.xlsx'))
    unique_cmps = [file for file in files_excel if 'unique_cmps' in os.path.basename(file)]
    for file in files_mzml_DDA:
        df2 = gen_DDA_ms2_df(file)
        name = os.path.basename(files_mzml_DDA[0]).split('DDA')[0][:-1] ###获得DDA文件的特征名称
        for file_excel in unique_cmps:
            if name in os.path.basename(file_excel):
                df1 = pd.read_excel(file_excel)
                for i in range(len(df1)):
                    rt,mz = df1.loc[i,['rt','mz']]
                    df_frag = df2[(df2['precursor']>=mz-0.015)&(df2['precursor']<=mz+0.015)
                        &(df2['rt']>=rt-0.1)&(df2['rt']<=rt+0.1)]
                    if len(df_frag)==0:
                        pass
                    else:
                        frag_all = []
                        for j in range(len(df_frag)):
                            mz1, intensity1 = df_frag['frag'].iloc[j]
                            frag_s = pd.Series(data=intensity1,index = mz1,dtype='float64')
                            frag_all.append(frag_s)
                        frag_s_all = pd.concat(frag_all).sort_values(ascending=False)
                        frag_s_all1 = frag_s_all[frag_s_all>200]
                        frag_s_all2=frag_s_all1[~frag_s_all1.index.duplicated(keep='first')]
                        frag_final = str(list(frag_s_all2.iloc[:20].index.values))
                        df1.loc[i,'frag_DDA'] = frag_final
                df1.to_excel(file_excel)            

    


if __name__ == '__main__':
    pass


