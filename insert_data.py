from adapter.inserting.csv import ImportCSV


if __name__ == '__main__':
    # create ImportCSV object
    import_csv: ImportCSV = ImportCSV()

    # customizable section
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # import data from csv file
    import_csv.insert(
        # set id and name of the group which the data should be connected to
        group_id=2, name="Kontrollgruppe",

        # mapping column from csv file to table column
        # write hir the column name of the csv file
        user_id_column_name="user_id", date_column_name="date", value_column_name="value"
    )
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
