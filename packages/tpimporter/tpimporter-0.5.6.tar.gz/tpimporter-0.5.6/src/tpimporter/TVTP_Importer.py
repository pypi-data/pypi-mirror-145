from .Excel_Importer import Excel_Importer
from openpyxl import Workbook
from typing import List, Dict, Tuple, Set


class TVTP_Importer(Excel_Importer):
    callback_status_signal = None
    callback_progress_signal = None

    # SPECIFY FIELDNAMES AND CORRESPONDING EXCEL COLUMN NUMBERs HERE
    tv_series_map = {
        "titel_local": 5,
        "titel_ov": 16,
        "vendor_id": 4,
        "vendor_id_amazon": 60,
        "vendor_id_google": 63,
        "vendor_id_videoload": 66,
        "vendor_id_hollystar": 72,
        "so_number": 147,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    tv_season_map = {
        "status": 0,
        "tnr": 1,
        "titel_local": 6,
        "number": 7,
        "no_of_episodes": 11,
        "deal_type": 15,
        "mandant": 27,
        "est_start": 37,
        "est_end": 38,
        "tvod_start": 40,
        "tvod_end": 41,
        "genre": 19,
        "rating": 20,
        "licensor": 14,
        "production_year": 17,
        "production_country": 18,
        "quality": 21,
        "tv_network": 32,
        "studio": 55,
        "vendor_id": 3,
        "vendor_id_itunes": 57,
        "vendor_id_amazon": 59,
        "vendor_id_google": 62,
        "vendor_id_videoload": 65,
        "vendor_id_maxdome": 68,
        "vendor_id_hollystar": 71,
        "initialprice_hd": 26,
        "initialprice_sd": 25,
        "initialprice_wsp_itunes_hd": 79,
        "initialprice_wsp_itunes_sd": 78,
        "initialprice_wsp_amazon_hd": 83,
        "initialprice_wsp_amazon_sd": 82,
        "country_de": 33,
        "country_at": 34,
        "country_ch": 35,
        "right_est": 36,
        "right_tvod": 39,
        "pf_status_videociety": 43,
        "pf_status_videobuster": 44,
        "pf_status_itunes": 45,
        "pf_status_amazon": 46,
        "pf_status_maxdome": 47,
        "pf_status_google": 48,
        "pf_status_videoload": 49,
        "pf_status_sky": 50,
        "pf_status_anime_on_demand": 51,
        "pf_status_hollystar": 53,
        "first_offer_date": 30,
        "so_number": 146,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    tv_episode_map = {
        "titel_local": 10,
        "number": 12,
        "rating": 20,
        "est_start": 37,
        "est_end": 38,
        "tvod_start": 40,
        "tvod_end": 41,
        "tv_air_date": 31,
        "runtime": 13,
        "vendor_id": 2,
        "vendor_id_itunes": 56,
        "vendor_id_amazon": 58,
        "vendor_id_google": 61,
        "vendor_id_videoload": 64,
        "vendor_id_maxdome": 67,
        "vendor_id_hollystar": 70,
        "initialprice_hd": 24,
        "initialprice_sd": 23,
        "initialprice_wsp_itunes_hd": 77,
        "initialprice_wsp_itunes_sd": 76,
        "initialprice_wsp_amazon_hd": 81,
        "initialprice_wsp_amazon_sd": 80,
        "so_number": 145,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    def __init__(self, valid_statuses=("ok", "change", "new")):
        super().__init__(valid_statuses)

    def get_tp_data_from_file(self, path) -> Dict:
        """
        imports the Titelplanung xlsm from a given filepath (String or Path)
        :param path: filepath (String or Path)
        :return: a list of dicts (one dict per title)
        """
        wb = self._load_workbook(path)
        return self._get_data_from_wb(wb)

    def _get_data_from_wb(self,
                          workbook: Workbook,
                          first_row: int = 4,
                          worksheet_name: str = "TPTV",
                          channel_type='transactional') -> Dict:
        """
        fetches data from the given Excel Workbook instance
        :param workbook: a Workbook instance
        :param first_row: the first row where we should expect the data to begin
        :param worksheet_name: name of the worksheet that should be read
        :param channel_type: possible values: transactional/filmtastic/arthousecnma/homeofhorror
        :return: a dictionary of all TV_Series --> every series is a dictionary that contains series info
        and under the key 'seasons' you'll find multiple dictionaries for all seasons of the series; likewise in every
        season you'll find the episodes under the key 'episodes'
        """
        series_data = dict()
        ws = workbook[worksheet_name]
        i = first_row
        max_row = ws.max_row
        print('max_row:', max_row)
        for row in ws['A' + str(first_row):'HB' + str(max_row)]:
            try:
                # progress (20 % schon nach öffnen erreicht)
                self.callback_progress(20 + int(i/max_row*80))

                # nur valide Items mit aktivem Status und einer Titelnummer nehmen
                if row[self.tv_season_map.get('tnr')].value and row[
                    self.tv_season_map.get('status')].value in self.valid_statuses:
                    # SERIES
                    series_dict = self._get_row_data(row=row,
                                                     item_map=self.tv_series_map,
                                                     channel_type=channel_type)
                    if not series_dict.get('vendor_id') in series_data.keys():
                        series_data[series_dict.get('vendor_id')] = series_dict

                    # SEASONS
                    if str(row[8].value).lower().strip() == 'x':
                        season_data = self._get_row_data(row=row,
                                                         item_map=self.tv_season_map,
                                                         channel_type=channel_type)
                        series = series_data.get(row[self.tv_series_map.get('vendor_id')].value)
                        if not 'seasons' in series.keys():
                            series['seasons'] = {
                                season_data.get('vendor_id'): season_data
                            }
                        else:
                            series['seasons'][season_data.get('vendor_id')] = season_data


                    # EPISODES
                    episode_data = self._get_row_data(row=row,
                                                           item_map=self.tv_episode_map,
                                                           channel_type=channel_type)
                    series = series_data.get(row[self.tv_series_map.get('vendor_id')].value)
                    season = series.get('seasons').get(row[self.tv_season_map.get('vendor_id')].value)
                    if not 'episodes' in season.keys():
                        season['episodes'] = {
                            episode_data.get('vendor_id'): episode_data
                        }
                    else:
                        season['episodes'][episode_data.get('vendor_id')] = episode_data

                i += 1

            except:
                self.callback_status(f'ERRROR reading in row nr: {i}')

        self.callback_progress(100)
        self.callback_status('reading data from TP - COMPLETE')
        return series_data

    def _get_row_data(self, row, item_map: dict, channel_type: str) -> dict:
        """
        reads in data from an Excel-row; specify the data you want within the item_map dictionary
        (field_name:Column-Number in Excel);
        :param row: an Excel row
        :param item_map: a dictionary (field_name:Column-Number in Excel)
        :param channel_type: String; possible values: transactional/filmtastic/arthousecnma/homeofhorror
        :return: dictionary with the keys from item_map and the corresponding values from the Excel row
        """
        row_data = dict()
        for key, col_nr in item_map.items():
            if key == 'channel_type':
                row_data[key] = channel_type
            else:
                try:
                    row_data[key] = row[col_nr].value
                    if row[col_nr].value == '#N/A':
                        row_data[key] = None
                except:
                    row_data[key] = ""
        return row_data
