from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.logic import Logic
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_rule_groups.rule_group import RuleGroup
from edc_rule_groups.predicate import P
from edc_rule_groups.decorators import register


@register()
class BaNamotsweRuleGroup(RuleGroup):

    crfs_artregimen = CrfRule(
        logic=Logic(
            predicate=P('arv_changes', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['artregimen'])

    crfs_tbhistory = CrfRule(
        logic=Logic(
            predicate=P('tb_diagnosis', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['tbhistory'])

    crfs_oi = CrfRule(
        logic=Logic(
            predicate=P('oi_diagnosis', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['oi'])

    crfs_pregnancyhistory = CrfRule(
        logic=Logic(
            predicate=P('preg_diagnosis', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['pregnancyhistory'])

    crfs_adherencecounselling = CrfRule(
        logic=Logic(
            predicate=P('counselling_adhere', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['adherencecounselling'])

    crfs_transferhistory = CrfRule(
        logic=Logic(
            predicate=P('transfer', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['transferhistory'])

    crfs_assessmenthistory = CrfRule(
        logic=Logic(
            predicate=P('assessment_history', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['assessmenthistory'])

    crfs_extraction = CrfRule(
        logic=Logic(
            predicate=P('extraction', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['extraction'])

    crfs_treatment = CrfRule(
        logic=Logic(
            predicate=P('treatment', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['treatment'])

    crfs_death = CrfRule(
        logic=Logic(
            predicate=P('death', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['death'])

    class Meta:
        app_label = 'ba_namotswe'
        source_model = 'ba_namotswe.extractionchecklist'
