from openfisca_us.model_api import *


class ctc_refundable_individual_maximum(Variable):
    value_type = float
    entity = Person
    label = "Maximum refundable CTC"
    unit = "currency-USD"
    documentation = "The maximum refundable CTC for this person."
    definition_period = YEAR
    reference = (
        "https://www.law.cornell.edu/uscode/text/26/24#a",
        "https://www.law.cornell.edu/uscode/text/26/24#h",
        "https://www.law.cornell.edu/uscode/text/26/24#i",
    )

    def formula(person, period, parameters):
        return person("ctc_individual_maximum", period)

    def formula_2018(person, period, parameters):
        amount = person("ctc_individual_maximum", period)
        ctc = parameters(period).irs.credits.ctc
        return min_(amount, ctc.refundable.individual_max)

    def formula_2021(person, period, parameters):
        return person("ctc_child_individual_maximum", period)

    formula_2022 = formula_2018

    formula_2026 = formula


class ctc_limiting_tax_liability(Variable):
    value_type = float
    entity = TaxUnit
    label = "CTC-limiting tax liability"
    unit = "currency-USD"
    documentation = "The tax liability used to determine the maximum amount of the non-refundable CTC."
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        non_refundable_credits = parameters(period).irs.credits.non_refundable
        total_credits = sum(
            [
                tax_unit(credit, period)
                for credit in non_refundable_credits
                if credit != "non_refundable_ctc"
            ]
        )
        return tax_unit("income_tax_before_credits", period) - total_credits


class refundable_ctc(Variable):
    value_type = float
    entity = TaxUnit
    label = "Refundable CTC"
    unit = "currency-USD"
    documentation = "The portion of the Child Tax Credit that is refundable."
    definition_period = YEAR
    reference = "https://www.law.cornell.edu/uscode/text/26/24#d"

    def formula(tax_unit, period, parameters):
        maximum_refundable_ctc = min_(
            aggr(tax_unit, period, ["ctc_refundable_individual_maximum"]),
            tax_unit("ctc", period),
        )

        liability = tax_unit("ctc_limiting_tax_liability", period)
        ctc = parameters(period).irs.credits.ctc
        earnings = aggr(tax_unit, period, ["earned_income"])
        earnings_over_threshold = max_(
            0, earnings - ctc.refundable.phase_in.threshold
        )
        relevant_earnings = (
            earnings_over_threshold * ctc.refundable.phase_in.rate
        )
        # Compute "social security taxes" as defined in the US Code for the ACTC.
        # This includes OASDI and Medicare payroll taxes, as well as half
        # of self-employment taxes.
        PERSON_VARIABLES = [
            "employee_social_security_tax",
            "employee_medicare_tax",
            "e09800",  # Unreported payroll tax.
        ]
        PERSON_VARIABLES_SUBTRACT = ["e11200"]  # Excess payroll tax withheld.
        TAX_UNIT_VARIABLES = [
            "c03260",  # Deductible portion of the self-employed tax.
            "additional_medicare_tax",
        ]
        social_security_tax = (
            aggr(tax_unit, period, PERSON_VARIABLES)
            + add(tax_unit, period, TAX_UNIT_VARIABLES)
            - aggr(tax_unit, period, PERSON_VARIABLES_SUBTRACT)
        )
        eitc = tax_unit("eitc", period)
        social_security_excess = max_(0, social_security_tax - eitc)

        phased_in_amount = max_(relevant_earnings, social_security_excess)

        capped_phase_in = min_(phased_in_amount, liability)
        return min_(capped_phase_in, maximum_refundable_ctc)

    def formula_2021(tax_unit, period, parameters):
        return aggr(tax_unit, period, ["ctc_refundable_individual_maximum"])

    formula_2022 = formula


class non_refundable_ctc(Variable):
    value_type = float
    entity = TaxUnit
    label = "Non-refundable CTC"
    unit = "currency-USD"
    documentation = (
        "The portion of the Child Tax Credit that is not refundable."
    )
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return tax_unit("ctc", period) - tax_unit("refundable_ctc", period)


c11070 = variable_alias("c11070", refundable_ctc)
