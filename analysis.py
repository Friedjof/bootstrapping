from causalimpact import CausalImpact

from adapter.analysis.causalimpact import Analyse
from modules.config import Configuration


if __name__ == '__main__':
    # create analysis object
    analysis: Analyse = Analyse(configuration=Configuration())

    # customizable section
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # get all samples from the database
    # you can set the sql command in the queries.py file
    analysis.get_samples(sql_command="final_aggregation")

    # serialize the samples
    print(analysis.serialized_rows)

    # plot the samples
    # you may have to change the pre_period and post_period
    ci = CausalImpact(analysis.serialized_rows, pre_period=[0, 4], post_period=[5, 10])
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # print a report of the causal impact
    print(ci.summary())
    print(ci.summary(output='report'))
    # visualize the causal impact
    ci.plot()
