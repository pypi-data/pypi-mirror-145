import numpy as np
import random
from pandas_plink import read_plink1_bin
genetic_data_path = "/ocean/projects/asc170022p/tighu/UKB_Genetic_Data/"


class genetic_data_handler:
    """
    A class to represent family of methods that can fetch list of xarray objects based on combination of list of
    subjects and variants provided

    """

    def __init__(self):

        genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + "1" + "_b0_v2.bed",
                                     genetic_data_path + "bim_files/" + "ukb_snp_chr" + "1" + "_v2.bim",
                                     genetic_data_path + "fam_files/" + "ukb22418_c" + "1" + "_b0_v2_s488176.fam",
                                     verbose=True)
        genetic_df = genetic_df.set_index({"variant": "snp"})
        self.all_ukb_subjects = genetic_df.sample.values

    def get_subject_ids(self):
        """
        A utility function which lets user fetch numpy array containing the list of all subject ids
        Parameters:
        No parameter required
        Returns:
        categories list: A numpy array object
        :rtype: np.ndarray
        """
        if self.all_ukb_subjects is None:
            print("Please initialize Module")
            return None

        else:
            return self.all_ukb_subjects

    @staticmethod
    def get_path_genetic_files():
        """
        A static function which lets user see all the genetic data locations

        Parameters:
        No parameter required

        Returns:
        categories list: A string
        :rtype: str
        """

        return genetic_data_path

    def get_genetic_data(self, subject_list=None, variant_dict=None):
        """ The Primary function of the module which allows user to provide a subject list and dictionary which has keys
            as chromosome numbers and values as a list of variants of interest. If no subjects list is provided 100
            random subjects are considered.If no dictionary is provided as input, an exception is raised.

                Parameters:
                subject_list (list str): List of subjects which are of interest
                variant_dict (dict): A python Dictionary having keys as relevant chromosome number and values as list of
                variants that are of interest to us.

                Returns:
                list: A python list of xarrayDatasets

        """
        if subject_list is None:

            subject_list = random.sample(self.all_ukb_subjects, 100)

        elif variant_dict is None:
            raise Exception

        genetic_data_array = []
        for chr_num in variant_dict.keys():

            genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + chr_num + "_b0_v2.bed",
                                         genetic_data_path + "bim_files/" + "ukb_snp_chr" + chr_num + "_v2.bim",
                                         genetic_data_path + "fam_files/" + "ukb22418_c" + chr_num +
                                         "_b0_v2_s488176.fam", verbose=True)

            genetic_df = genetic_df.set_index({"variant": "snp"})
            genetic_df = genetic_df.where(genetic_df['sample'].isin(subject_list) & genetic_df['variant'].isin(
                variant_dict[chr_num]), drop=True)

            genetic_data_array.append(genetic_df)

        return genetic_data_array
