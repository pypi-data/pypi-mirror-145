'''
ext_Experiment is the container for whole project data.
Heavy lifting is in constructors.CompositeMap, 
    which contains MassGrid for correspondence, and FeatureList from feature/peak detection.
Annotation is facilitated by jms-metabolite-services, mass2chem.
Format of a sample: {
            'input_file': file,
            'ion_mode': parameters['mode'],
            # below will be populated after processing
            'name': '',
            'list_scan_numbers': [],
            'list_retention_time': [],
            'list_mass_tracks': [], 
            'anchor_mz_pairs': [],                    # mostly isotopic pairs to establish m/z anchors (landmarks)
            'number_anchor_mz_pairs': -1,
        } 
        
'''
import random
import multiprocessing as mp

import pymzml
from jms.io import read_table_to_peaks
from mass2chem.epdsConstructor import epdsConstructor

from .experiment import *
from .chromatograms import extract_massTracks_        # extract_massTracks, 
from .mass_functions import *
from .samples import get_file_masstrack_stats

# -----------------------------------------------------------------------------

def register_samples(list_input_files):
    '''
    Establish sample_id here, return sample_registry as a dictionary.
    '''
    sample_registry = {}
    ii = 0
    for file in sorted(list_input_files):
        sample_registry[ii] = {'sample_id': ii, 'input_file': file}
        ii += 1
    return sample_registry

def process_project(list_input_files, parameters):
    '''
    list_input_files: Extracted ion chromatogram files.
    parameters: dictionary of most parameters.
    sample_registry include: 'status:mzml_parsing', 'status:eic', 'number_anchor_mz_pairs', 
                'data_location', track_mzs: (mz, masstrack_id)

    '''
    sample_registry = register_samples(list_input_files)
    shared_dict = batch_EIC_from_samples_ondisk(sample_registry, parameters)
    for sid, sam in sample_registry.items():
        sam['status:mzml_parsing'], sam['status:eic'], sam['number_anchor_mz_pairs'
                ], sam['data_location'], sam['track_mzs'] = shared_dict[sid]

        sam['name'] = os.path.basename(sam['input_file']).replace('.mzML', '')
    
    # print(sample_registry)
    EE = ext_Experiment(sample_registry, parameters)
    EE.process_all()
    EE.export_all()

# -----------------------------------------------------------------------------
# Subcommand functions

def analyze_single_sample(infile, 
            mz_tolerance_ppm=5, min_intensity=100, min_timepoints=5, min_peak_height=1000,
            parameters={}):
    '''
    Analyze single mzML file and print statistics.
    parameters are not used, just place holder to use ext_Experiment class.

    to add output info on instrumentation

    '''
    print("Analysis of %s\n" %infile)
    mz_landmarks, mode, min_peak_height_ = get_file_masstrack_stats(infile,
                mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height)

    EE = ext_Experiment({}, parameters)
    EE.load_annotation_db()
    mass_accuracy_ratio = EE.KCD.evaluate_mass_accuracy_ratio(mz_landmarks, mode, mz_tolerance_ppm=10)
    # print("  Mass accuracy is estimated as %2.1f ppm." %(mass_accuracy_ratio*1000000))
    print("\n")


def estimate_min_peak_height(list_input_files, 
            mz_tolerance_ppm=5, min_intensity=100, min_timepoints=5, min_peak_height=500,
            num_files_to_use=3):
    '''
    return an estimated parameter for min peak_height as half of the min verified landmark peaks.
    '''
    estimated = []
    if len(list_input_files) <= num_files_to_use:
        selected = list_input_files
    else:
        selected = random.sample(list_input_files, num_files_to_use)
    print("Estimating parameter for min peak_height based on ", selected)
    for infile in selected:
        try:
            mz_landmarks, mode, min_peak_height_ = get_file_masstrack_stats(infile,
                        mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height)
                        # not all above parameters are used or relevant
            estimated.append(min_peak_height_)
        except:
            print("Error in analyzing ", infile)
    recommended = int(0.5 * np.median(estimated))
    print("Estimated parameter for min peak_height is %d \n" %recommended)
    return recommended

def ext_estimate_min_peak_height(list_input_files, 
            mz_tolerance_ppm=5, min_intensity=100, min_timepoints=5, min_peak_height=500,
            num_files_to_use=3):
    '''
    return dict of
    ion mode and
    an estimated parameter for min peak_height as half of the min verified landmark peaks.
    Extended estimate_min_peak_height for X-asari use.
    '''
    estimated, _ionmode = [], []
    if len(list_input_files) <= num_files_to_use:
        selected = list_input_files
    else:
        selected = random.sample(list_input_files, num_files_to_use)
    print("Estimating parameter for min peak_height based on ", selected)
    for infile in selected:
        try:
            mz_landmarks, mode, min_peak_height_ = get_file_masstrack_stats(infile,
                        mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height)
                        # not all above parameters are used or relevant
            estimated.append(min_peak_height_)
            _ionmode.append(mode)
        except:
            print("Error in analyzing ", infile)
    recommended = int(0.5 * np.median(estimated))
    if len(set(_ionmode)) > 1:
        print("Error occured due to inconsistent ion mode." )
        print(selected, _ionmode)
        return None
    else:
        return {'mode': _ionmode[0], 'min_peak_height': recommended}

def annotate_user_featuretable(infile, parameters):
                        # mode='pos', mz_tolerance_ppm=5):
    '''
    infile: tab delimited file with first row as header, first column m/z and 2nd column rtime.
    output: two files in current directory, Feature_annotation.tsv and Annotated_empricalCompounds.json

    def is_coeluted_by_distance(P1, P2, rt_tolerance=10):
        _coeluted = False
        if abs(P1['apex']-P2['apex']) <= rt_tolerance:
            _coeluted = True
        return _coeluted

    '''
    parameters['outdir'] = ''
    mode = parameters['mode']
    list_peaks = read_table_to_peaks(infile, 
                                has_header=True, mz_col=0, rtime_col=1, feature_id=None ,
                                )
    # print("Read %d features." %len(list_peaks))
    EE = ext_Experiment({}, parameters)
    EE.load_annotation_db()
    ECCON = epdsConstructor(list_peaks, mode=mode)
    EED = ExperimentalEcpdDatabase(mode=mode)
    EED.dict_empCpds = ECCON.peaks_to_epdDict(
                seed_search_patterns = ECCON.seed_search_patterns, 
                ext_search_patterns = ECCON.ext_search_patterns,
                mz_tolerance_ppm= parameters['mz_tolerance_ppm'], 
                coelution_function='distance',
                check_isotope_ratio = False
                ) 
    EED.index_empCpds()
    EED.extend_empCpd_annotation(EE.KCD)
    EED.annotate_singletons(EE.KCD)

    EE.export_peak_annotation(EED.dict_empCpds, EE.KCD, 'Feature_annotation')
    # also exporting JSON
    with open('Annotated_empricalCompounds.json', 'w', encoding='utf-8') as f:
        json.dump(EED.dict_empCpds, f, cls=NpEncoder, ensure_ascii=False, indent=2)

# -----------------------------------------------------------------------------
# Multi-core functions

def make_iter_parameters(sample_registry, parameters, shared_dict):
    '''
    Generate iterables for multiprocess.starmap for getting sample mass tracks.
    return:
    [('sample_id', input_file, mode, mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height, output_file, shared_dict), ...]
    '''
    iters = []
    mz_tolerance_ppm = parameters['mz_tolerance']
    min_intensity = parameters['min_intensity_threshold']
    min_timepoints = parameters['min_timepoints']
    min_peak_height = parameters['min_peak_height']
    for sample in sample_registry.values():
        iters.append(
            (sample['sample_id'], sample['input_file'], parameters['mode'],
            mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height,
            os.path.join(parameters['outdir'], 'pickle', os.path.basename(sample['input_file']).replace('.mzML', '')+'.pickle'),
            shared_dict
            )
        )
    return iters


def batch_EIC_from_samples_in_memory(sample_registry, parameters):
    pass

def batch_EIC_from_samples_to_mongo(sample_registry, parameters, cursor):
    pass



def batch_EIC_from_samples_ondisk(sample_registry, parameters):
    '''
    multiprocessing of mass track extraction of samples, and return shared_dict.
    More anchors mean better coverage of features, helpful to select reference sample.
    '''
    with mp.Manager() as manager:
        shared_dict = manager.dict()
        iters = make_iter_parameters(sample_registry, parameters, shared_dict)
        # print("Number of processes ", number_processes)
        with mp.Pool( parameters['multicores'] ) as pool:
            pool.starmap( single_sample_EICs_ondisk, iters )

        _d = dict(shared_dict)
    return _d

def single_sample_EICs_ondisk(sample_id, infile, ion_mode, 
                    mz_tolerance_ppm, min_intensity, min_timepoints, min_peak_height, outfile, shared_dict):

    '''
    Process infile. `shared_dict` is used to pass back information, 
    sample_id: ('mzml_parsing', 'eic', number_anchor_mz_pairs, outfile, track_mzs)
    track_mzs are used later for aligning m/z tracks.
    '''
    new = {'sample_id': sample_id, 'input_file': infile, 'ion_mode': ion_mode,}
    list_mass_tracks = []
    track_mzs = []
    try:
        exp = pymzml.run.Reader(infile)
        xdict = extract_massTracks_(exp, 
                    mz_tolerance_ppm=mz_tolerance_ppm, 
                    min_intensity=min_intensity, 
                    min_timepoints=min_timepoints, 
                    min_peak_height=min_peak_height)
        new['list_scan_numbers'] = xdict['rt_numbers']            # list of scans, starting from 0
        new['list_retention_time'] = xdict['rt_times']        # full RT time points in sample
        ii = 0
        # already in ascending order of m/z from extract_massTracks_, get_thousandth_regions
        for track in xdict['tracks']:                         
            list_mass_tracks.append( {
                'id_number': ii, 
                'mz': track[0],
                'rt_scan_numbers': track[1], 
                'intensity': track[2], 
                } )
            track_mzs.append( (track[0], ii) )                  # keep a reconrd in sample registry for fast MassGrid align
            ii += 1

        new['list_mass_tracks'] = list_mass_tracks
        anchor_mz_pairs = find_mzdiff_pairs_from_masstracks(list_mass_tracks, mz_tolerance_ppm=mz_tolerance_ppm)
        new['anchor_mz_pairs'] = anchor_mz_pairs
        new['number_anchor_mz_pairs'] = len(anchor_mz_pairs)
        shared_dict[new['sample_id']] = ('passed', 'passed', new['number_anchor_mz_pairs'], outfile, track_mzs)
    
        with open(outfile, 'wb') as f:
            pickle.dump(new, f, pickle.HIGHEST_PROTOCOL)

        print("Processed %s with %d mass tracks." %(os.path.basename(infile), ii))

    except:
        shared_dict[new['sample_id']] = ('failed', '', 0, '', [])
        print("mzML processing error in sample %s, skipped." %infile)
