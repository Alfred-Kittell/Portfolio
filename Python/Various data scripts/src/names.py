"""Разные имена и группы имён"""


"""UUID трансформаторов"""
guids_equipment = \
    {
        "064256ce-d896-432a-998e-9cdff66cde0e": "Белый Раст Т-6",  # Белый Раст Т-6
        "992f5774-f6b7-4da1-a01a-bf0c6fb79e19": "Белый Раст Т-7",  # Белый Раст Т-7
        "684b9c34-b783-4410-8fc9-bd659ad54947": "044",  # Бескудниково АТ-2
        "3d9edc60-7587-4046-ac83-8a516a6809c1": "049",  # Бескудниково Т-1
        "9a771e40-df99-4768-9faf-707e8c214a82": "050",  # Бескудниково Т-2
        "ae2bcc12-8e54-4b5b-857b-682180f623f4": "051",  # Бескудниково Т-3
        "408d2d8f-b831-4586-89f0-13f7099de142": "052",  # Бескудниково Т-4
        "88118457-ad38-44a3-922e-fa85fd4feb6b": "057",  # Очаково АТ-1
        "0a79c752-21bc-4ce6-82f5-6d8e438b6bb4": "058",  # Очаково АТ-2
        "d39469c2-4179-4f94-917a-a4bce433d958": "059",  # Очаково АТ-3
        "448a4a6f-1392-4a7e-97b9-de0d2d470f55": "060",  # Очаково АТ-4
        "60bcb44e-0c23-4cc7-9d55-d1017fdd3f27": "061",  # Очаково АТ-5
        "9f95bc3b-45de-4b34-9eca-401f391a8810": "062",  # Очаково АТ-6
        "1db38820-efb2-489f-8291-15a3c2bf84c7": "063",  # Очаково АТ-7
        "26670a9b-bf38-472c-a0f8-0db8de84ab0e": "064",  # Очаково АТ-10
        "ba6856d1-aa65-4f5b-a531-81f6c0777035": "065",  # Очаково АТ-11
        "65f8945a-250e-4225-93c9-324870a6ee86": "066",  # Очаково Т-8
        "ad9aaa4e-1913-46ed-affa-55d7768f1fb2": "067",  # Очаково Т-9
        "8af4283c-04cd-4ad3-b44d-af0eb56bcf66": "068",  # Очаково Т-12
        "d9476e5f-41b9-47fb-8850-78af1e55a298": "069",  # Очаково Т-13
        "27a34981-365a-43c4-a3d7-781e916c1190": "Пахра Т-5",  # Пахра Т-5
        "322b04fe-22da-4a4f-804d-fad0ee325f6d": "Пахра Т-6",  # Пахра Т-6
        # тестовые объекты продукта общие
        "2c9cb593-5048-4fd0-884d-3fc512591b9a": "TT_HV_13_08",
        "86324cb3-c112-4105-8275-0ab6b06e2a2f":	"TT_MV_13_08",
        "40bb6385-1e2f-44b4-b4df-c0a559ce113c":	"TT_LV_13_08",
        "be094c30-30a6-4ad1-a386-1b3fa980f050":	"TT_A1_15_08",
        "d67447e4-13fe-4e3c-9bba-11b46d4d72d5":	"Т-4",
        "53a91a60-a5dd-4052-af4a-e4aec962e6cc":	"Т-3",
        "316ba1d5-9999-47e8-9fb2-e73aa726d7f3":	"Т-2",
        "c1235374-1daa-4e06-9b81-e1eb51cf51a4":	"gis-400",
        "2d18ca12-1b40-43b9-af1b-13a7b39d3833":	"Т-1",
        "ee037632-2067-48b5-b469-fc4ea7474c7e":	"Т1",
        "3ee6e5fd-80a4-4ead-bf56-54bcf9be9a45":	"Т4",
        "8c092394-fd18-4f98-a81b-d63d058a661e":	"Т3",
        "007c4d75-2201-425f-8414-08db5804ba3c":	"Т2",
        "84a60215-8e44-4ec6-ba69-25780b56afc6":	"GIS-400",
        # тестовые объекты продукта рус
        "ec5c4649-40f6-4e9b-9185-d0b700c5f4e8":	"T-A1",
        "c536a7af-fcc3-4ff2-8066-b5785838f535":	"Гузар-500 - АТ-1 A",
        "5f1ab1d2-22df-4635-8d94-46a727aec285":	"Гузар-500 - АТ-2 A",
        "4d62c6a8-9fa4-4c98-a702-1f6af06d6664":	"Гузар-500 - АТ-2 B",
        "c63977e2-1737-444a-8ecb-10078ed7cb56":	"Гузар-500 - АТ-2 C",
        "ff077bcd-0863-4aff-8cb4-36c9607ddca5":	"Гузар-500 - АТ-1 C",
        "e95a0ca9-909d-46ec-8a7f-b4523821c063":	"Гузар-500 - АТ-1 B",
        "8d342c63-5294-4908-a841-ed2d81b3ebd2":	"T-87",
    }

"""UUID сигналов"""
guids_parameter = \
    {
        "0646b549-cafd-4358-bd19-81488bf52a3d":  "c_co",  # Концентрации растворённых газов: оксид углерода
        "0f76d94d-a6f7-472e-8323-5c7333e511d2":  "c_co2",  # Концентрации растворённых газов: диоксид углерода
        "d9061974-402e-40d1-ad54-75fd8b9e6b1c":  "c_ch4",  # Концентрации растворённых газов: метан
        "23e66a4a-a209-470d-9cb7-1d0649c0c067":  "c_c2h2",  # Концентрации растворённых газов: ацетилен
        "f0b83a66-a76d-453a-ad6d-1235a9bc8695":  "c_c2h4",  # Концентрации растворённых газов: этилен
        "182860d6-f8a1-49c1-8a92-f002eb900de0":  "c_c2h6",  # Концентрации растворённых газов: этан
        "2fe10048-bd2b-4e56-bd87-3370499a10e1":  "c_h2",  # Концентрации растворённых газов: водород
        "866a355a-7cf1-4f77-a6a3-27defe252449":  "rs",  # Относительное значение влагосодержания
        "5b76111a-ebc4-41b9-b4bc-2d7dcfe4743b":  "t_bt",  # Температура нижних слоёв
        "7a56e1f6-ae92-4e0e-9786-ec08d4d24511":  "t_tp",  # Температура верхних слоёв
    }

"""UUID прибора, параметр + трансформатор"""
guids_meter = \
    {
        "0646b549-cafd-4358-bd19-81488bf52a3d":  "c_co",  # Концентрации растворённых газов: оксид углерода
        "0f76d94d-a6f7-472e-8323-5c7333e511d2":  "c_co2",  # Концентрации растворённых газов: диоксид углерода
        "d9061974-402e-40d1-ad54-75fd8b9e6b1c":  "c_ch4",  # Концентрации растворённых газов: метан
        "23e66a4a-a209-470d-9cb7-1d0649c0c067":  "c_c2h2",  # Концентрации растворённых газов: ацетилен
        "f0b83a66-a76d-453a-ad6d-1235a9bc8695":  "c_c2h4",  # Концентрации растворённых газов: этилен
        "182860d6-f8a1-49c1-8a92-f002eb900de0":  "c_c2h6",  # Концентрации растворённых газов: этан
        "2fe10048-bd2b-4e56-bd87-3370499a10e1":  "c_h2",  # Концентрации растворённых газов: водород
        "866a355a-7cf1-4f77-a6a3-27defe252449":  "rs",  # Относительное значение влагосодержания
        "5b76111a-ebc4-41b9-b4bc-2d7dcfe4743b":  "t_bt",  # Температура нижних слоёв
        "7a56e1f6-ae92-4e0e-9786-ec08d4d24511":  "t_tp",  # Температура верхних слоёв
    }

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

"""Правильные имена из ранних датасетов"""
columnFilter = \
    [
        ['С2Н2', 'С2Н2'],
        ['С2Н4', 'С2Н4'],
        ['С2Н6', 'С2Н6'],
        ['СН4', 'СН4'],
        ['СО', 'СО'],
        ['Н2', 'Н2'],
        ['СО2', 'СО2'],
        ['ТОКФАЗАА', 'Ток фаза А'],
        ['ТОКФАЗАВ', 'Ток фаза В'],
        ['ТОКФАЗАС', 'Ток фаза С'],
        ['МОЩНОСТЬАКТИВНАЯ', 'Мощность активная'],
        ['МОЩНОСТЬРЕАКТИВНАЯ', 'Мощность реактивная'],
        ['МОЩНОСТЬПОЛНАЯ', 'Мощность полная'],
        ['ТЕМПЕРАТУРАВЕРХ', 'Температура верх'],
        ['ТЕМПЕРАТУРАНИЗ', 'Температура низ'],
        ['ТЕМПЕРАТУРАОКРСРЕДЫ', 'Температура окр среды'],
        ['ВЛАЖНОСТЬМАСЛАОТН', 'Влажность масла отн']
    ]

"""Полный набор параметров из 7hi"""
# columns_7hi = \
#     [
#         ['datetime', 'datetime'],
#         ['H2', 'c_h2'],
#         ['O2', 'c_o2'],
#         ['CH4', 'c_ch4'],
#         ['CO', 'c_co'],
#         ['C2H4', 'c_c2h4'],
#         ['C2H6', 'c_c2h6'],
#         ['C2H2', 'c_c2h2'],
#         ['CO2', 'c_co2'],
#         ['Tair', 't_en'],
#         ['Toil', 't_bt'],
#         ['cn', 'cn'],
#         ['dAf', 'dAf'],
#         ['wF', 'wF'],
#         ['cS', 'cS'],
#         ['uRF', 'uRF'],
#         ['uPAF', 'uPAF'],
#         ['uAF', 'uAF'],
#         ['uSF', 'uSF'],
#         ['def', 'def'],
#         ['C3H8', 'C3H8'],
#         ['C3H6', 'C3H6'],
#         ['N2', 'N2'],
#         ['sH2', 'sH2'],
#         ['sCH4', 'sCH4'],
#         ['sCO', 'sCO'],
#         ['sC2H4', 'sC2H4'],
#         ['sC2H2', 'sC2H2'],
#         ['sCO2', 'sCO2'],
#         ['sH2O', 'sH2O'],
#         ['H2O_in', 'H2O_in'],  # humrel_lq, rs
#         ['H2O_out', 'H2O_out'],
#         ['T_out', 'T_out'],
#         ['Nitro', 'Nitro'],
#         ['C2H2_C2H4', 'C2H2_C2H4'],
#         ['CH4_H2', 'CH4_H2'],
#         ['C2H4_C2H6', 'C2H4_C2H6'],
#         ['Tpneu', 'Tpneu'],
#         ['Tted', 'Tted'],
#         ['Tkol', 'Tkol'],
#         ['P_S1', 'P_S1'],
#         ['Tsam', 'Tsam'],
#         ['Trad', 'Trad'],
#         ['Tmain', 'Tmain'],
#         ['GA_P1', 'GA_P1'],
#         ['GA_P2', 'GA_P2'],
#         ['TH2Oin', 'TH2Oin'],
#         ['Fgaz', 'Fgaz'],
#         ['HistoryClearCompleted', 'HistoryClearCompleted'],
#         ['adat11', 'adat11'],
#         ['adat12', 'adat12'],
#         ['adat13', 'adat13'],
#     ]

"""Только важные из 7hi"""
columns_7hi_v1 = \
    [
        ['datetime', 'datetime'],
        ['C2H2', 'c_c2h2'],
        ['C2H4', 'c_c2h4'],
        ['C2H6', 'c_c2h6'],
        ['CH4', 'c_ch4'],
        ['CO', 'c_co'],
        ['CO2', 'c_co2'],
        ['H2', 'c_h2'],
        ['Tair', 't_en'],
        #['Toil', 'Температура низ'],  # вероятно внутрення температура
        ['H2O_in', 'rs'],  # humrel_lq, rs
    ]

"""Только важные из 7hi"""
columns_7hi_v2 = \
    [
        ['datetime', 'datetime'],
        ['C2H2', 'c2h2'],
        ['C2H4', 'c2h4'],
        ['C2H6', 'c2h6'],
        ['CH4', 'ch4'],
        ['CO', 'co'],
        ['H2', 'h2'],
        ['CO2', 'co2'],
        #['O2', 'o2'],
        #['N2', 'n2'],
        ['Tair', 't_a'],
        #"['Toil', 't_o_bot_m'], t nj  # вероятно внутрення температура
        ['H2O_in', 'Влажность масла отн'],  # humrel_lq, rs
    ]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

"""Запрос для снятия данных - Стачка """
condition_087 = ''
columns_087 = [
    #[table, dt_Org, dt_Need, col_Org, col_Need, condition]
    ["measurement_dga", '"data"+"time"', "datetime", "h2", "c_h2", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "co", "c_co", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "co2", "c_co2", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "ch4", "c_ch4", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h2", "c_c2h2", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h4", "c_c2h4", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h6", "c_c2h6", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_h2", "c_roc_h2_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_co", "c_roc_co_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_co2", "c_roc_co2_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_ch4", "c_roc_ch4_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_c2h2", "c_roc_c2h2_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_c2h4", "c_roc_c2h4_abs", condition_087],
    ["measurement_dga", '"data"+"time"', "datetime", "va30_c2h6", "c_roc_c2h6_abs", condition_087],
    ["measurement_h2o", '"data"+"time"', "datetime", "rs", "rs", condition_087],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcl", "wcl", condition_087],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcp", "wcp", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "t_a", "t_en", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_bot_m", "t_bt", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_top_m", "t_tp", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_hv", "i_hv_pa", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_hv", "i_hv_pb", condition_087],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_hv", "i_hv_pc", condition_087],
]

"""Запрос для снятия данных -  """
condition_088 = 'WHERE "id_disp" = 6667'
columns_088 = [
    #[table, dt_Org, dt_Need, col_Org, col_Need, condition]
    ["measurement_dga", '"data"+"time"', "datetime", "h2", "c_h2", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "co", "c_co", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "co2", "c_co2", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "ch4", "c_ch4", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h2", "c_c2h2", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h4", "c_c2h4", condition_088],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h6", "c_c2h6", condition_088],
    ["measurement_h2o", '"data"+"time"', "datetime", "rs", "rs", condition_088],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcl", "wcl", condition_088],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcp", "wcp", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "t_a", "t_en", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_bot_m", "t_bt", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_top_m", "t_tp", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_hv", "i_pa_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_hv", "i_pb_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_hv", "i_pc_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_mv", "i_pa_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_mv", "i_pb_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_mv", "i_pc_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_lv", "i_pa_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_lv", "i_pb_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_lv", "i_pc_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_hv", "u_pa_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_hv", "u_pb_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_hv", "u_pc_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_mv", "u_pa_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_mv", "u_pb_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_mv", "u_pc_mv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_lv", "u_pa_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_lv", "u_pb_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_lv", "u_pc_lv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "p_hv", "p_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "q_hv", "q_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "s_hv", "s_hv", condition_088],
    ["measurement_e", '"data"+"Time"', "datetime", "cos_hv", "cos_hv", condition_088],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_a", "tg_delta_pa", condition_088],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_b", "tg_delta_pb", condition_088],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_c", "tg_delta_pc", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_a", "d_tg_delta_pa", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_b", "d_tg_delta_pb", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_c", "d_tg_delta_pc", condition_088],
    ["measurement_bushings", "date_time", "datetime", "c_a", "c1_pa", condition_088],
    ["measurement_bushings", "date_time", "datetime", "c_b", "c1_pb", condition_088],
    ["measurement_bushings", "date_time", "datetime", "c_c", "c1_pc", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_c_a", "d_c1_pa", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_c_b", "d_c1_pb", condition_088],
    ["measurement_bushings", "date_time", "datetime", "d_c_c", "d_c1_pc", condition_088],
]

"""Запрос для снятия данных -  """
condition_089 = 'WHERE "id_disp" = 6668'
columns_089 = [
    #[table, dt_Org, dt_Need, col_Org, col_Need, condition]
    ["measurement_dga", '"data"+"time"', "datetime", "h2", "c_h2", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "co", "c_co", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "co2", "c_co2", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "ch4", "c_ch4", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h2", "c_c2h2", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h4", "c_c2h4", condition_089],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h6", "c_c2h6", condition_089],
    ["measurement_h2o", '"data"+"time"', "datetime", "rs", "rs", condition_089],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcl", "wcl", condition_089],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcp", "wcp", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "t_a", "t_en", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_bot_m", "t_bt", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_top_m", "t_tp", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_hv", "i_pa_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_hv", "i_pb_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_hv", "i_pc_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_mv", "i_pa_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_mv", "i_pb_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_mv", "i_pc_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_lv", "i_pa_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_lv", "i_pb_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_lv", "i_pc_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_hv", "u_pa_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_hv", "u_pb_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_hv", "u_pc_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_mv", "u_pa_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_mv", "u_pb_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_mv", "u_pc_mv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_lv", "u_pa_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_lv", "u_pb_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_lv", "u_pc_lv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "p_hv", "p_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "q_hv", "q_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "s_hv", "s_hv", condition_089],
    ["measurement_e", '"data"+"Time"', "datetime", "cos_hv", "cos_hv", condition_089],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_a", "tg_delta_pa", condition_089],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_b", "tg_delta_pb", condition_089],
    ["measurement_bushings", "date_time", "datetime", "tg_delta_c", "tg_delta_pc", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_a", "d_tg_delta_pa", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_b", "d_tg_delta_pb", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_tg_delta_c", "d_tg_delta_pc", condition_089],
    ["measurement_bushings", "date_time", "datetime", "c_a", "c1_pa", condition_089],
    ["measurement_bushings", "date_time", "datetime", "c_b", "c1_pb", condition_089],
    ["measurement_bushings", "date_time", "datetime", "c_c", "c1_pc", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_c_a", "d_c1_pa", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_c_b", "d_c1_pb", condition_089],
    ["measurement_bushings", "date_time", "datetime", "d_c_c", "d_c1_pc", condition_089],
]

"""Запрос для снятия данных -  """
condition_092 = 'WHERE "id_disp" = 6668'
columns_092 = [
    #[table, dt_Org, dt_Need, col_Org, col_Need, condition]
    ["measurement_dga", '"data"+"time"', "datetime", "h2", "c_h2", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "co", "c_co", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "co2", "c_co2", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "ch4", "c_ch4", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h2", "c_c2h2", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h4", "c_c2h4", condition_092],
    ["measurement_dga", '"data"+"time"', "datetime", "c2h6", "c_c2h6", condition_092],
    ["measurement_h2o", '"data"+"time"', "datetime", "rs", "rs", condition_092],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcl", "wcl", condition_092],
    ["measurement_h2o", '"data"+"time"', "datetime", "wcp", "wcp", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "t_a", "t_en", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_bot_m", "t_bt", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "t_o_top_m", "t_tp", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_hv", "i_pa_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_hv", "i_pb_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_hv", "i_pc_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_mv", "i_pa_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_mv", "i_pb_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_mv", "i_pc_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ia_lv", "i_pa_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ib_lv", "i_pb_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ic_lv", "i_pc_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_hv", "u_pa_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_hv", "u_pb_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_hv", "u_pc_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_mv", "u_pa_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_mv", "u_pb_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_mv", "u_pc_mv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ua_lv", "u_pa_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "ub_lv", "u_pb_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "uc_lv", "u_pc_lv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "p_hv", "p_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "q_hv", "q_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "s_hv", "s_hv", condition_092],
    ["measurement_e", '"data"+"Time"', "datetime", "cos_hv", "cos_hv", condition_092],
]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

"""Объекты и подстанции ЕС АСМД"""
all_assets = {
    "ПС Ленинградская": [
        "АТ-1 ф.A",
        "АТ-1 ф.B",
        "АТ-1 ф.C",
        "Р-1 ф.A",
        "Р-1 ф.B",
        "Р-1 ф.C",
    ],
    "ПС Звёздная": [
        "КЛ-330",
    ],
    "ПС Очаково": [
        "АТ-1",
        "АТ-2",
        "АТ-3",
        "АТ-4",
        "АТ-5",
        "АТ-6",
        "АТ-7",
        "АТ-10",
        "АТ-11",
        "Т-8",
        "Т-9",
        "Т-12",
        "Т-13",
        "КРУЭ-500"
    ],
    "ПС Белый Раст": [
        "АТ-5",
    ],
    "ПС Бескудниково": [
        "АТ-1",
        "АТ-2",
        "АТ-3",
        "АТ-4",
        "АТ-5",
        "АТ-6",
        "Т-1",
        "Т-2",
        "Т-3",
        "Т-4",
    ],
    "ПС Пахра": [
        "АТ-1",
        "АТ-2",
    ]
}

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

"""Коды сигналов"""
SIGNALS = {
    'A-Slot22': {
        # end winding
        'status-C1': 'pd_a_22ew_status',  # Статус замера
        'dtime-C1': 'pd_a_22ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_a_22ew_prpd',  # Датчик ЧР SSC4, фаза A, паз №22, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_a_22ew_nqn_pos',  # Датчик ЧР SSC4, фаза A, паз №22, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_a_22ew_nqn_neg',  # Датчик ЧР SSC4, фаза A, паз №22, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_a_22ew_qm_pos',  # Датчик ЧР SSC4, фаза A, паз №22, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_a_22ew_qm_neg',  # Датчик ЧР SSC4, фаза A, паз №22, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_a_22s_status',  # Статус замера
        'dtime-C2': 'pd_a_22s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_a_22s_prpd',  # Датчик ЧР SSC4, фаза A, паз №22, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_a_22s_nqn_pos',  # Датчик ЧР SSC4, фаза A, паз №22, общий, NQN+
        'nqnNeg-C2': 'pd_a_22s_nqn_neg',  # Датчик ЧР SSC4, фаза A, паз №22, общий, NQN-
        'qmPos-C2': 'pd_a_22s_qm_pos',  # Датчик ЧР SSC4, фаза A, паз №22, общий, Qm+
        'qmNeg-C2': 'pd_a_22s_qm_neg',  # Датчик ЧР SSC4, фаза A, паз №22, общий, Qm-
    },
    'A2-Slot7': {
        # end winding
        'status-C1': 'pd_a_7ew_status',  # Статус замера
        'dtime-C1': 'pd_a_7ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_a_7ew_prpd',  # Датчик ЧР SSC1, фаза A, паз №7, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_a_7ew_nqn_pos',  # Датчик ЧР SSC1, фаза A, паз №7, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_a_7ew_nqn_neg',  # Датчик ЧР SSC1, фаза A, паз №7, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_a_7ew_qm_pos',  # Датчик ЧР SSC1, фаза A, паз №7, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_a_7ew_qm_neg',  # Датчик ЧР SSC1, фаза A, паз №7, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_a_7s_status',  # Статус замера
        'dtime-C2': 'pd_a_7s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_a_7s_prpd',  # Датчик ЧР SSC1, фаза A, паз №7, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_a_7s_nqn_pos',  # Датчик ЧР SSC1, фаза A, паз №7, общий, NQN+
        'nqnNeg-C2': 'pd_a_7s_nqn_neg',  # Датчик ЧР SSC1, фаза A, паз №7, общий, NQN-
        'qmPos-C2': 'pd_a_7s_qm_pos',  # Датчик ЧР SSC1, фаза A, паз №7, общий, Qm+
        'qmNeg-C2': 'pd_a_7s_qm_neg',  # Датчик ЧР SSC1, фаза A, паз №7, общий, Qm-
    },
    'B-Slot36': {
        # end winding
        'status-C1': 'pd_b_36ew_status',  # Статус замера
        'dtime-C1': 'pd_b_36ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_b_36ew_prpd',  # Датчик ЧР SSC6, фаза B, паз №36, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_b_36ew_nqn_pos',  # Датчик ЧР SSC6, фаза B, паз №36, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_b_36ew_nqn_neg',  # Датчик ЧР SSC6, фаза B, паз №36, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_b_36ew_qm_pos',  # Датчик ЧР SSC6, фаза B, паз №36, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_b_36ew_qm_neg',  # Датчик ЧР SSC6, фаза B, паз №36, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_b_36s_status',  # Статус замера
        'dtime-C2': 'pd_b_36s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_b_36s_prpd',  # Датчик ЧР SSC6, фаза B, паз №36, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_b_36s_nqn_pos',  # Датчик ЧР SSC6, фаза B, паз №36, общий, NQN+
        'nqnNeg-C2': 'pd_b_36s_nqn_neg',  # Датчик ЧР SSC6, фаза B, паз №36, общий, NQN-
        'qmPos-C2': 'pd_b_36s_qm_pos',  # Датчик ЧР SSC6, фаза B, паз №36, общий, Qm+
        'qmNeg-C2': 'pd_b_36s_qm_neg',  # Датчик ЧР SSC6, фаза B, паз №36, общий, Qm-
    },
    'B2-Slot21': {
        # end winding
        'status-C1': 'pd_b_21ew_status',  # Статус замера
        'dtime-C1': 'pd_b_21ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_b_21ew_prpd',  # Датчик ЧР SSC3, фаза B, паз №21, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_b_21ew_nqn_pos',  # Датчик ЧР SSC3, фаза B, паз №21, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_b_21ew_nqn_neg',  # Датчик ЧР SSC3, фаза B, паз №21, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_b_21ew_qm_pos',  # Датчик ЧР SSC3, фаза B, паз №21, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_b_21ew_qm_neg',  # Датчик ЧР SSC3, фаза B, паз №21, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_b_21s_status',  # Статус замера
        'dtime-C2': 'pd_b_21s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_b_21s_prpd',  # Датчик ЧР SSC3, фаза B, паз №21, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_b_21s_nqn_pos',  # Датчик ЧР SSC3, фаза B, паз №21, общий, NQN+
        'nqnNeg-C2': 'pd_b_21s_nqn_neg',  # Датчик ЧР SSC3, фаза B, паз №21, общий, NQN-
        'qmPos-C2': 'pd_b_21s_qm_pos',  # Датчик ЧР SSC3, фаза B, паз №21, общий, Qm+
        'qmNeg-C2': 'pd_b_21s_qm_neg',  # Датчик ЧР SSC3, фаза B, паз №21, общий, Qm-
    },
    'C-Slot8': {
        # end winding
        'status-C1': 'pd_c_8ew_status',  # Статус замера
        'dtime-C1': 'pd_c_8ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_c_8ew_prpd',  # Датчик ЧР SSC2, фаза C, паз №8, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_c_8ew_nqn_pos',  # Датчик ЧР SSC2, фаза C, паз №8, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_c_8ew_nqn_neg',  # Датчик ЧР SSC2, фаза C, паз №8, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_c_8ew_qm_pos',  # Датчик ЧР SSC2, фаза C, паз №8, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_c_8ew_qm_neg',  # Датчик ЧР SSC2, фаза C, паз №8, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_c_8s_status',  # Статус замера
        'dtime-C2': 'pd_c_8s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_c_8s_prpd',  # Датчик ЧР SSC2, фаза C, паз №8, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_c_8s_nqn_pos',  # Датчик ЧР SSC2, фаза C, паз №8, общий, NQN+
        'nqnNeg-C2': 'pd_c_8s_nqn_neg',  # Датчик ЧР SSC2, фаза C, паз №8, общий, NQN-
        'qmPos-C2': 'pd_c_8s_qm_pos',  # Датчик ЧР SSC2, фаза C, паз №8, общий, Qm+
        'qmNeg-C2': 'pd_c_8s_qm_neg',  # Датчик ЧР SSC2, фаза C, паз №8, общий, Qm-
    },
    'C2-Slot35': {
        # end winding
        'status-C1': 'pd_c_35ew_status',  # Статус замера
        'dtime-C1': 'pd_c_35ew_dtime',  # Метка времени замера
        'PRPD-C1': 'pd_c_35ew_prpd',  # Датчик ЧР SSC5, фаза C, паз №35, лобовая часть обмотки, PRPD-диаграмма
        'nqnPos-C1': 'pd_c_35ew_nqn_pos',  # Датчик ЧР SSC5, фаза C, паз №35, лобовая часть обмотки, NQN+
        'nqnNeg-C1': 'pd_c_35ew_nqn_neg',  # Датчик ЧР SSC5, фаза C, паз №35, лобовая часть обмотки, NQN-
        'qmPos-C1': 'pd_c_35ew_qm_pos',  # Датчик ЧР SSC5, фаза C, паз №35, лобовая часть обмотки, Qm+
        'qmNeg-C1': 'pd_c_35ew_qm_neg',  # Датчик ЧР SSC5, фаза C, паз №35, лобовая часть обмотки, Qm-
        # slot total
        'status-C2': 'pd_c_35s_status',  # Статус замера
        'dtime-C2': 'pd_c_35s_dtime',  # Метка времени замера
        'PRPD-C2': 'pd_c_35s_prpd',  # Датчик ЧР SSC5, фаза C, паз №35, общий, PRPD-диаграмма
        'nqnPos-C2': 'pd_c_35s_nqn_pos',  # Датчик ЧР SSC5, фаза C, паз №35, общий, NQN+
        'nqnNeg-C2': 'pd_c_35s_nqn_neg',  # Датчик ЧР SSC5, фаза C, паз №35, общий, NQN-
        'qmPos-C2': 'pd_c_35s_qm_pos',  # Датчик ЧР SSC5, фаза C, паз №35, общий, Qm+
        'qmNeg-C2': 'pd_c_35s_qm_neg',  # Датчик ЧР SSC5, фаза C, паз №35, общий, Qm-
    }
}

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def create_master_dict():
    """Генерация мастер-словаря авто сортировщика"""
    master_dict = {"timestamp": 0, "datetime": 1}

    # Группы
    phases = [
        "pa",  # фаза A
        "pb",  # фаза B
        "pc",  # фаза C
        "hv",  # высокая сторона
        "mv",  # средняя сторона
        "lv",  # низкая сторона
        "ltc",  # рпн
        "pa_hv",  # фаза A, высокая сторона
        "pb_hv",  # фаза B, высокая сторона
        "pc_hv",  # фаза C, высокая сторона
        "pa_hv_1",  # фаза A, высокая сторона
        "pb_hv_1",  # фаза B, высокая сторона
        "pc_hv_1",  # фаза C, высокая сторона
        "pspare_hv",  # фаза резервная, высокая сторона
        "pa_mv",  # фаза A, средняя сторона
        "pb_mv",  # фаза B, средняя сторона
        "pc_mv",  # фаза C, средняя сторона
        "pspare_mv",  # фаза резервная, средняя сторона
        "pa_lv",  # фаза A, низкая сторона
        "pb_lv",  # фаза B, низкая сторона
        "pc_lv",  # фаза C, низкая сторона
        "pa_lv_1",  # фаза A, низкая сторона
        "pb_lv_1",  # фаза B, низкая сторона
        "pc_lv_1",  # фаза C, низкая сторона
        "pa_lv_2",  # фаза A, низкая сторона
        "pb_lv_2",  # фаза B, низкая сторона
        "pc_lv_2",  # фаза C, низкая сторона
        "pspare_lv",  # фаза резервная, низкая сторона
        "ltc_pa_hv",  # рпн, фаза A, высокая сторона
        "ltc_pb_hv",  # рпн, фаза B, высокая сторона
        "ltc_pc_hv",  # рпн, фаза C, высокая сторона
        "ltc_pspare_hv",  # рпн, фаза резервная, высокая сторона
        "ltc_pa_mv",  # рпн, фаза A, средняя сторона
        "ltc_pb_mv",  # рпн, фаза B, средняя сторона
        "ltc_pc_mv",  # рпн, фаза C, средняя сторона
        "ltc_pspare_mv",  # рпн, фаза резервная, средняя сторона
        "ltc_pa_lv",  # рпн, фаза A, низкая сторона
        "ltc_pb_lv",  # рпн, фаза B, низкая сторона
        "ltc_pc_lv",  # рпн, фаза C, низкая сторона
        "ltc_pspare_lv",  # рпн, фаза резервная, низкая сторона
    ]
    growths = [
        "roc_abs_day",  # Скорость роста абсолютная, сутки
        "roc_rel_day",  # Скорость роста относительная, сутки
        "roc_abs_week",  # Скорость роста абсолютная, неделя
        "roc_rel_week",  # Скорость роста относительная, неделя
        "roc_abs_month",  # Скорость роста абсолютная, месяц
        "roc_rel_month",  # Скорость роста относительная, месяц
        "roc_abs_year",  # Скорость роста абсолютная, год
        "roc_rel_year",  # Скорость роста относительная, год
    ]
    gases = [
        "h2",  # Водород
        "o2",  # Кислород
        "n2",  # Азот
        "co",  # Угарный газ
        "co2",  # Углекислый газ
        "ch4",  # Метан
        "c2h2",  # Ацетилен
        "c2h4",  # Этилен
        "c2h6",  # Этан
        "ch",  # Сумма углеводородных газов
        "tg",  # Сумма растворённых газов
        "tcg",  # Сумма горючих газов
        "thg",  # Сумма теплового газа
        "tdcg",  # Сумма горючих газов и CO
        "tcgh2",  # Сумма горючих газов и водорода
    ]
    humidity = [
        "rs",  # Влажность относительная масла, %
        "rs_2",  # Влажность относительная масла, %
        "rs_s",  # Относительное влагонасыщение масла
        "rs_en",  #
        "wcl",  # Влажность абсолютная масла, ppm
        "wcl_s",  # Максимальная влажность абсолютная масла, ppm
        "wcp",  # Влажность абсолютная бумаги, %
    ]
    temperature = [
        "t_en",  # Температура окружающего воздуха
        "t_bt",  # Температура нижних слоёв масла
        "t_tp",  # Температура верхних слоёв масла
        "t_hst",  # Температура наиболее нагретой точки (ТННТ)
        "t_cb",  # Температура в шкафу
        "t_bl",  # Температура образования пузырьков
        "t_cn",  # Температура конденсации влаги
        "t_om",  # Температура в газоанализиторе
        "t_ltc",  # Температура масла в контакторе РПН
        "t_mn",  # Температура в блоке мониторинга
        "t_winding_akm",  # Температура обмотки (АКМ)
        "t_oil_akm",  # Температура масла (АКМ)
        "t_flash",  # Температура вспышки
    ]
    electrical = [
        [
            "i",  # Ток
            "i_leak_active",  # Ток
            "i_leak_reactive",  # Ток
            "u",  # Напряжение фазное
            "u_breakdown",  # Напряжение фазное
        ],
        [
            "u_pab",  # Напряжение линейное AB
            "u_pbc",  # Напряжение линейное BC
            "u_pca",  # Напряжение линейное CA
        ],
        [
            "p",  # (Суммарная) Мощность активная
            "q",  # (Суммарная) Мощность реактивная
            "s",  # (Суммарная) Мощность полная
            "coeff_load",  # Коэф. нагрузки
            "cos_phi",  # Угол диэлектрических потерь
        ]
    ]
    bushing = [
        "bush_tgd",  # Тангенс угла диэлектрических потерь основной изоляции ввода
        "bush_tgd_avg",  # Тангенс угла диэлектрических потерь основной изоляции ввода среднее
        "bush_tgd_20",  # Тангенс угла диэлектрических потерь основной изоляции ввода при t=20 ˚C (не более), %
        "bush_tgd_70",  # Тангенс угла диэлектрических потерь основной изоляции ввода при t=70 ˚C (не более), %
        "bush_tgd_90",  # Тангенс угла диэлектрических потерь основной изоляции ввода при t=90 ˚C (не более), %
        "bush_d_tgd",  # Изменение тангенса угла диэлектрических потерь основной изоляции ввода
        "bush_d_tgd_avg",  # Изменение тангенса угла диэлектрических потерь основной изоляции ввода среднее
        "bush_c1",  # Ёмкость основной изоляции ввода
        "bush_c1_avg",  # Ёмкость основной изоляции ввода среднее
        "bush_c1_20",  # Ёмкость основной изоляции ввода для 20 град.
        "bush_d_c1",  # Изменение ёмкости основной изоляции
        "bush_d_c1_avg",  # Изменение ёмкости основной 1изоляции среднее
        "bush_pd_level",  # Уровень ЧР изоляции ввода
        "bush_imbalance_phase",  # Фаза вектора небаланса
        "bush_i_creepage",  # Ток утечки по поверхности ввода
        "bush_i_leakage",  # Ток утечки через основную изоляцию ввода
    ]
    rpn = [
       "ltc_pos",  # Положение РПН
       "ltc_electrical_wear",  # Отн. эл. износ контактов РПН
       "ltc_mechanical_wear",  # Положение РПН
    ]
    its = [
        "d_hi",  # Вклад онлайн-параметров в ИТС
    ]
    cooling = [
        "cooling_heatflow",  #
        "cooling_t_in",  #
        "cooling_t_out",  #
    ]
    universal = [
        "koh",  # Кислотное число
        "contents_debris",  # Содержание мехпримесей
    ]

    def fill(main, sub, pref="", mid="", post="", reverse=False):
        """Шаблон наполнения"""
        for m in main:
            for s in sub:
                if not s:
                    name = f"{pref}{m}{post}"
                elif not reverse:
                    name = f"{pref}{m}{mid}{s}{post}"
                else:
                    name = f"{pref}{s}{mid}{m}{post}"
                if name in master_dict:
                    print(f"duplicate: {name}")
                else:
                    master_dict[name] = len(master_dict)

    # Правила формирования
    rules = [
        # Газы
        (gases, [""]+phases, "c_", "_", ""),
        (gases, [""]+phases, "c_", "_", "_offline"),
        (gases, ["avg_day"], "", "_", ""),
        (growths, gases, "c_", "_", "", True),
        # Влага
        (humidity, [""]+phases, "", "_", ""),
        (humidity, [""], "", "_", "_local"),
        (humidity, [""]+phases, "", "_", "_offline"),
        (humidity, ["avg_day"], "", "_", ""),
        (growths, humidity, "", "_", "", True),
        # Температуры
        (temperature, [""]+phases, "", "_", ""),
        (temperature, [""], "", "_", "_local"),
        (temperature, [""]+phases, "", "_", "_offline"),
        # Электричество
        (electrical[0], [""]+phases, "", "_", ""),
        (["hv", "mv", "lv", "lv_1", "lv_2"], electrical[1], "", "_", "", True),
        (electrical[2], [""]+phases, "", "_", ""),
        (electrical[0], [""]+phases, "", "_", "_offline"),
        (["hv", "mv", "lv", "lv_1", "lv_2"], electrical[1], "", "_", "_offline", True),
        (electrical[2], [""]+phases, "", "_", "_local"),
        (electrical[2], [""]+phases, "", "_", "_offline"),
        # Ввода
        (bushing, [""]+phases, "", "_", ""),
        (bushing, [""]+phases, "", "_", "_offline"),
        # РПН
        (rpn, [""]+phases, "", "_", ""),
        (rpn, [""]+phases, "", "_", "_local"),
        (rpn, [""]+phases, "", "_", "_offline"),
        # ИТС
        (its, [""]+phases, "", "_", ""),
        (its, [""]+phases, "", "_", "_offline"),
        # Охлаждение
        (cooling, ["1", "2", "3", "4"], "", "_", ""),
        (cooling, ["1", "2", "3", "4"], "", "_", "_offline"),
        # Общие
        (universal, [""], "", "_", ""),
        (universal, [""], "", "_", "_offline"),
    ]
    # Наполнение
    for rule in rules:
        fill(*rule)

    return master_dict


def create_rename_map(columns):
    """Генерация мастер-словаря авто переименования"""
    rename_map = {}

    # Правила для фаз
    phases = [
        [["_hv_pab", "_vn_pab", "_pab_vn"], "_pab_hv"],  # фаза AB
        [["_mv_pab", "_sn_pab", "_pab_sn"], "_pab_mv"],
        [["_lv_pab", "_ln_pab", "_pab_ln"], "_pab_lv"],
        [["_hv_pbc", "_vn_pbc", "_pbc_vn"], "_pbc_hv"],  # фаза BC
        [["_mv_pbc", "_sn_pbc", "_pbc_sn"], "_pbc_mv"],
        [["_lv_pbc", "_ln_pbc", "_pbc_ln"], "_pbc_lv"],
        [["_hv_pca", "_vn_pca", "_pca_vn"], "_pca_hv"],  # фаза CA
        [["_mv_pca", "_sn_pca", "_pca_sn"], "_pca_mv"],
        [["_lv_pca", "_ln_pca", "_pca_ln"], "_pca_lv"],
        [["_hv1_pab", "_vn1_pab", "_pab_vn1"], "_pab_hv_1"],  # фаза AB
        [["_mv1_pab", "_sn1_pab", "_pab_sn1"], "_pab_mv_1"],
        [["_lv1_pab", "_ln1_pab", "_pab_ln1"], "_pab_lv_1"],
        [["_hv1_pbc", "_vn1_pbc", "_pbc_vn1"], "_pbc_hv_1"],  # фаза BC
        [["_mv1_pbc", "_sn1_pbc", "_pbc_sn1"], "_pbc_mv_1"],
        [["_lv1_pbc", "_ln1_pbc", "_pbc_ln1"], "_pbc_lv_1"],
        [["_hv1_pca", "_vn1_pca", "_pca_vn1"], "_pca_hv_1"],  # фаза CA
        [["_mv1_pca", "_sn1_pca", "_pca_sn1"], "_pca_mv_1"],
        [["_lv1_pca", "_ln1_pca", "_pca_ln1"], "_pca_lv_1"],
        [["_hv2_pab", "_vn2_pab", "_pab_vn2"], "_pab_hv_2"],  # фаза AB
        [["_mv2_pab", "_sn2_pab", "_pab_sn2"], "_pab_mv_2"],
        [["_lv2_pab", "_ln2_pab", "_pab_ln2"], "_pab_lv_2"],
        [["_hv2_pbc", "_vn2_pbc", "_pbc_vn2"], "_pbc_hv_2"],  # фаза BC
        [["_mv2_pbc", "_sn2_pbc", "_pbc_sn2"], "_pbc_mv_2"],
        [["_lv2_pbc", "_ln2_pbc", "_pbc_ln2"], "_pbc_lv_2"],
        [["_hv2_pca", "_vn2_pca", "_pca_vn2"], "_pca_hv_2"],  # фаза CA
        [["_mv2_pca", "_sn2_pca", "_pca_sn2"], "_pca_mv_2"],
        [["_lv2_pca", "_ln2_pca", "_pca_ln2"], "_pca_lv_2"],
        [["_hv_pa", "_vn_pa", "_pa_vn"], "_pa_hv"],  # фаза A
        [["_mv_pa", "_sn_pa", "_pa_sn"], "_pa_mv"],
        [["_lv_pa", "_ln_pa", "_pa_ln"], "_pa_lv"],
        [["_hv_pb", "_vn_pb", "_pb_vn"], "_pb_hv"],  # фаза B
        [["_mv_pb", "_sn_pb", "_pb_sn"], "_pb_mv"],
        [["_lv_pb", "_ln_pb", "_pb_ln"], "_pb_lv"],
        [["_hv_pc", "_vn_pc", "_pc_vn"], "_pc_hv"],  # фаза C
        [["_mv_pc", "_sn_pc", "_pc_sn"], "_pc_mv"],
        [["_lv_pc", "_ln_pc", "_pc_ln"], "_pc_lv"],
        [["_hv1_pa", "_vn1_pa", "_pa_vn1"], "_pa_hv_1"],  # фаза A
        [["_mv1_pa", "_sn1_pa", "_pa_sn1"], "_pa_mv_1"],
        [["_lv1_pa", "_ln1_pa", "_pa_ln1"], "_pa_lv_1"],
        [["_hv1_pb", "_vn1_pb", "_pb_vn1"], "_pb_hv_1"],  # фаза B
        [["_mv1_pb", "_sn1_pb", "_pb_sn1"], "_pb_mv_1"],
        [["_lv1_pb", "_ln1_pb", "_pb_ln1"], "_pb_lv_1"],
        [["_hv1_pc", "_vn1_pc", "_pc_vn1"], "_pc_hv_1"],  # фаза C
        [["_mv1_pc", "_sn1_pc", "_pc_sn1"], "_pc_mv_1"],
        [["_lv1_pc", "_ln1_pc", "_pc_ln1"], "_pc_lv_1"],
        [["_hv2_pa", "_vn2_pa", "_pa_vn2"], "_pa_hv_2"],  # фаза A
        [["_mv2_pa", "_sn2_pa", "_pa_sn2"], "_pa_mv_2"],
        [["_lv2_pa", "_ln2_pa", "_pa_ln2"], "_pa_lv_2"],
        [["_hv2_pb", "_vn2_pb", "_pb_vn2"], "_pb_hv_2"],  # фаза B
        [["_mv2_pb", "_sn2_pb", "_pb_sn2"], "_pb_mv_2"],
        [["_lv2_pb", "_ln2_pb", "_pb_ln2"], "_pb_lv_2"],
        [["_hv2_pc", "_vn2_pc", "_pc_vn2"], "_pc_hv_2"],  # фаза C
        [["_mv2_pc", "_sn2_pc", "_pc_sn2"], "_pc_mv_2"],
        [["_lv2_pc", "_ln2_pc", "_pc_ln2"], "_pc_lv_2"],
        [["_hv_pspare", "_pspare_pc", "_pspare_vn"], "_pspare_hv"],  # фаза резервная
        [["_mv_pspare", "_pspare_pc", "_pspare_sn"], "_pspare_mv"],
        [["_lv_pspare", "_pspare_pc", "_pspare_ln"], "_pspare_lv"],
    ]
    # Группы
    growths = [
        "abs_day",  # Скорость роста абсолютная, сутки
        "rel_day",  # Скорость роста относительная, сутки
        "abs_week",  # Скорость роста абсолютная, неделя
        "rel_week",  # Скорость роста относительная, неделя
        "abs_month",  # Скорость роста абсолютная, месяц
        "rel_month",  # Скорость роста относительная, месяц
        "abs_year",  # Скорость роста абсолютная, год
        "rel_year",  # Скорость роста относительная, год
    ]
    gases = [
        "h2",  # Водород
        "o2",  # Кислород
        "n2",  # Азот
        "co",  # Угарный газ
        "co2",  # Углекислый газ
        "ch4",  # Метан
        "c2h2",  # Ацетилен
        "c2h4",  # Этилен
        "c2h6",  # Этан
        "ch",  # Сумма углеводородных газов
        "tg",  # Сумма растворённых газов
        "tcg",  # Сумма горючих газов
        "thg",  # Сумма теплового газа
        "tdсg",  # Сумма горючих газов и CO
        "tcgh2",  # Сумма горючих газов и водорода
    ]
    humidity = [
        "rs",  # Влажность относительная масла, %
        "rs_s",  # Относительное влагонасыщение масла
        "wcl",  # Влажность абсолютная масла, ppm
        "wcl_s",  # Максимальная влажность абсолютная масла, ppm
        "wcp",  # Влажность абсолютная бумаги, %
    ]

    # Правила для скоростей
    growths_dict = {}
    for grow in growths:
        for gas in gases:
            good = f"c_{gas}_roc_{grow}"
            bad = f"c_roc_{gas}_{grow}"
            growths_dict[bad] = good

    # Правила для влажности
    humidity_dict = {}
    for grow in growths:
        for hum in humidity:
            bad_grow = grow[:3]+"_roc"+grow[3:]
            good = f"{hum}_roc_{grow}"
            bad = f"{hum}_{bad_grow}"
            humidity_dict[bad] = good

    for col in columns:
        newcol = col
        if "_roc_" in col:
            if newcol in growths_dict:
                newcol = growths_dict.get(col, col)
            if newcol in humidity_dict:
                newcol = humidity_dict.get(col, col)
        else:
            for names, rep in phases:
                found = None
                for name in names:
                    if name in col:
                        found = name
                        break
                if found:
                    newcol = col.replace(found, rep)
                    break
            if col.endswith("_off") and not col.startswith("cooling"):
                newcol = col.replace("_off", "_offline")
        if newcol != col:
            print(f"\t\t{col} -> {newcol}")
            rename_map[col] = newcol

    return rename_map

