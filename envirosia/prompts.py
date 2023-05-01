class EquityESGPrompt:
    template = """
    Your task is to produce an ESG analysis of the following companies: {company_names} \
    
    ESG data is provided for each company separately below, delimited by triple backticks. \
    Focus only on four of the companies, specifically:
    - the two riskiest (low ESG scores) companies 
    - the two least risky (high ESG scores) companies

    For each of these four companies, write two contiguous sections.

    For the first section, summarise the corresponding JSON data, which is delimited by \
    triple backticks. Do not list everything out and do not mention you are using data from this JSON.\
    In particular, compare the ratings and scores from Sustainalytics, \
    Refinitiv, MSCI and ISS to see if they are consistent. \
    In the same section, analyse historical trends where applicable, and if data is available on the implied temperature \
    rise, mention if this is consistent with the Paris agreement of <1.5. Also mention SDG alignment if any are available.\
    Additionally, use 'exec_ages' to determine the proportion of gender and age diversity on the board in a single sentence. \
    Do not mention that this could lead to incorrect conclusions. \

    For the second section, summarise any past ESG controversies of this company. \
    For each controversy, make sure to mention the year and exact parties involved. Also summarise \
    any major projects, products or social initiatives and whether they are \
    beneficial or detrimental to sustainability and long-term growth. \
    """

    def __init__(self, company_names: list, data: list[dict]):
        self.company_names = company_names
        self.data = data
    
    def prompt(self):
        output = self.template.format(company_names = self.company_names)
        for company_data in self.data:
            output += f" ```{company_data}``` "
        return output

class FundESGPrompt:
    template = """
    Your task is to write a analysis of  {name}. There should be two sections, \
    but do not name the sections explicitly. \
     
    For the first section, summarise the description below, \
    which is delimited by triple backticks. If this is unavailable,\
    use existing information instead. \

    For the second section, analyse the ESG agenda of the firm which runs or owns this fund \
    (e.g. for ishares it would be Blackrock) \
    based on their primary goals (e.g. decarbonsation targets) and \
    any past ESG controversies. For the controversies, make sure to mention \
    specific dates and parties involved.
    ```{description}```
    """

    def __init__(self, name: str, description: list):
        self.name = name
        self.description = description
        self.prompt = self.template.format(name=self.name, description=self.description)

# class EquityESGPrompt:
#     template = """
#     Your task is to produce an ESG analysis of the following companies: {company_names} \
    
#     ESG data is provided for each company separately below, delimited by triple backticks. \
#     For each company, write two sections.

#     For the first section, summarise the corresponding JSON data, which is delimited by \
#     triple backticks. Do not list everything out and do not mention you are using data from this JSON.\
#     In particular, compare the ratings and scores from Sustainalytics, \
#     Refinitiv, MSCI and ISS to see if they are consistent. \
#     In the same section, analyse historical trends where applicable, and if data is available on the implied temperature \
#     rise, mention if this is consistent with the Paris agreement of <1.5. Also mention SDG alignment if any are available.\
#     Additionally, use 'exec_ages' to determine the proportion of gender and age diversity on the board in a single sentence. \
#     Do not mention that this could lead to incorrect conclusions. \

#     For the second section, summarise any past ESG controversies of this company. \
#     For each controversy, make sure to mention the year and exact parties involved. Also summarise \
#     any major projects, products or social initiatives and whether they are \
#     beneficial or detrimental to sustainability and long-term growth. \
#     """

#     def __init__(self, company_names: list, data: list[dict]):
#         self.company_names = company_names
#         self.data = data
    
#     def prompt(self):
#         output = self.template.format(company_names = self.company_names)
#         for company_data in self.data:
#             output += f" ```{company_data}``` "
#         return output

# prompt for async analysis of individual holdings

# class EquityESGPrompt:
#     template = """
#     Your task is to write an ESG report with two sections for {name}, \
#     but do not name the sections explicitly. \
#     Format the report as follows: \
#     {ticker} <contents of report> \

#     For the first section, summarise the JSON data below for {name}, which is delimited by \
#     triple backticks. Do not list everything out and do not mention you are using data from this JSON.\
#     In particular, compare the ratings and scores from Sustainalytics, \
#     Refinitiv, MSCI and ISS to see if they are consistent. \
#     In the same section, analyse historical trends where applicable, and if data is available on the implied temperature \
#     rise, mention if this is consistent with the Paris agreement of <1.5. Also mention SDG alignment if any are available.\
#     Additionally, use 'exec_ages' to determine the proportion of gender and age diversity on the board in a single sentence. \
#     Do not mention that this could lead to incorrect conclusions. \

#     For the second section, summarise any past ESG controversies of {name}. For each controversy, \
#     make sure to mention the year and exact parties involved. Also summarise \
#     any major projects, products or social initiatives of {name} and whether they are \
#     beneficial or detrimental to sustainability and long-term growth.
#     ```{data}```
#     """

#     def __init__(self, name: str, ticker: str, data: dict):
#         self.name = name
#         self.ticker = ticker
#         self.data = data
#         self.prompt = self.template.format(name=self.name, ticker = self.ticker, data=self.data)
