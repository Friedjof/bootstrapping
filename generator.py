import datetime

from toolbox.generator.generate_testdata import Generator


if __name__ == '__main__':
    # customize section
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # create generator object
    # you can set the start_date, date_steps, start_user_id, group_id, value_range
    data_generator = Generator(
        start_date=datetime.date(1970, 1, 1),
        date_steps=datetime.timedelta(days=1),
        start_user_id=1, group_id=1, value_range=(0, 100)
    )
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # generate data
    data_generator.generate_data()
