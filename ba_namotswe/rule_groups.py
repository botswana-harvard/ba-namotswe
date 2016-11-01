# from edc_rule_groups.crf_rule import CrfRule
# from edc_rule_groups.logic import Logic
# from edc_metadata.constants import REQUIRED, NOT_REQUIRED
# from edc_rule_groups.rule_group import RuleGroup
# from edc_rule_groups.predicate import P
# from edc_rule_groups.decorators import register
# from edc_constants.constants import FEMALE
# 
# 
# @register()
# class EntryToCareRuleGroup(RuleGroup):
# 
#     crf_pregnancy = CrfRule(
#         logic=Logic(
#             predicate=P('gender', 'eq', FEMALE),
#             consequence=REQUIRED,
#             alternative=NOT_REQUIRED),
#         target_models=['pregnancyhistory'])
# 
#     class Meta:
#         app_label = 'ba_namotswe'
#         source_model = 'ba_namotswe.entrytocare'
# 
# 
# @register()
# class InCareRuleGroup(RuleGroup):
# 
#     crf_pregnancy = CrfRule(
#         logic=Logic(
#             predicate=P('gender', 'eq', FEMALE),
#             consequence=REQUIRED,
#             alternative=NOT_REQUIRED),
#         target_models=['pregnancyhistory'])
# 
#     class Meta:
#         app_label = 'ba_namotswe'
#         source_model = 'ba_namotswe.incare'
