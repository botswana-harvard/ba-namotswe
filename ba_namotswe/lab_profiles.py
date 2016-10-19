from edc_lab.aliquot.processing_profile import ProcessingProfile
from edc_lab.lab_profile import LabProfile
from edc_lab.requisition.requisition_panel import RequisitionPanel
from edc_lab.site_lab_profiles import site_lab_profiles

from .models import AliquotType


lab_profile = LabProfile('clinic_lab')

pl = AliquotType('Plasma', 'PL', '36')
lab_profile.add_aliquot_type(pl)

bc = AliquotType('Buffy Coat', 'BC', '12')
lab_profile.add_aliquot_type(bc)

wb = AliquotType('Whole Blood', 'WB', '02')
wb.add_derivative(bc)
wb.add_derivative(pl)
lab_profile.add_aliquot_type(wb)

viral_load_processing = ProcessingProfile('viral_load', wb)
viral_load_processing.add_process(pl, 4)
viral_load_processing.add_process(bc, 3)
lab_profile.add_processing_profile(viral_load_processing)

pbmc_processing = ProcessingProfile('pbmc', wb)
pbmc_processing.add_process(pl, 4)
lab_profile.add_processing_profile(pbmc_processing)

viral_load_panel = RequisitionPanel('Viral Load', wb)  # link this to the visit_schedule
viral_load_panel.processing_profile = viral_load_processing
lab_profile.add_panel(viral_load_panel)

hema_panel = RequisitionPanel('Hematology', wb)  # link this to the visit_schedule
lab_profile.add_panel(hema_panel)

urina_panel = RequisitionPanel('Urinalysis', wb)  # link this to the visit_schedule
lab_profile.add_panel(urina_panel)

syphillis_panel = RequisitionPanel('Syphillis', wb)  # link this to the visit_schedule
lab_profile.add_panel(syphillis_panel)

vl_iso_seq_panel = RequisitionPanel('Viral Isolation/Sequencing', wb)  # link this to the visit_schedule
lab_profile.add_panel(vl_iso_seq_panel)

hema_arv_panel = RequisitionPanel('Hematology (ARV)', wb)  # link this to the visit_schedule
lab_profile.add_panel(hema_arv_panel)

vrc_panel = RequisitionPanel('VRC01 Ab Levels', wb)  # link this to the visit_schedule
lab_profile.add_panel(vrc_panel)

serum_panel = RequisitionPanel('Serum', wb)  # link this to the visit_schedule
lab_profile.add_panel(serum_panel)

func_homoral_panel = RequisitionPanel('Functional Humoral Assays(STORAGE)', wb)  # link this to the visit_schedule
lab_profile.add_panel(func_homoral_panel)

dbs_panel = RequisitionPanel('Dried Blood Spot', 'DBS', '01')
lab_profile.add_panel(dbs_panel)

hiv_diagnostics_panel = RequisitionPanel('HIV Diagnostics', 'WB')
lab_profile.add_panel(hiv_diagnostics_panel)

cd4_arv_panel = RequisitionPanel('CD4 (ARV)', wb)  # link this to the visit_schedule
lab_profile.add_panel(cd4_arv_panel)

chem_nvp_panel = RequisitionPanel('Chemistry NVP/LFT + ALPL6 (ARV)', wb)  # link this to the visit_schedule
lab_profile.add_panel(chem_nvp_panel)

chem_panel = RequisitionPanel('Chemistry', wb)  # link this to the visit_schedule
lab_profile.add_panel(chem_panel)

chem_non_lpv_panel = RequisitionPanel('BHP086 Chemistry NON-LPV', wb)  # link this to the visit_schedule
lab_profile.add_panel(chem_non_lpv_panel)

dna_pcr_panel = RequisitionPanel('ELISA', wb)  # link this to the visit_schedule
lab_profile.add_panel(dna_pcr_panel)

pharma_cokienetics_panel = RequisitionPanel('Pharmacokinetics', wb)  # link this to the visit_schedule
lab_profile.add_panel(pharma_cokienetics_panel)

pbmc_panel = RequisitionPanel('PBMC', wb)  # link this to the visit_schedule
lab_profile.add_panel(pbmc_panel)

pl_and_coat_panel = RequisitionPanel('Plasma and Buffy Coat Storage', wb)  # link this to the visit_schedule
lab_profile.add_panel(pl_and_coat_panel)

hiv_genotyping_panel = RequisitionPanel('HIV Genotyping', wb)  # link this to the visit_schedule
lab_profile.add_panel(hiv_genotyping_panel)

rdb_panel = RequisitionPanel('Research Blood Draw', wb)  # link this to the visit_schedule
lab_profile.add_panel(rdb_panel)

site_lab_profiles.register('ba_namotswe.subjectrequisition', lab_profile)
