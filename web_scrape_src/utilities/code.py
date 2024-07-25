def save_ds_file(wanted_file_name, file=None,):
    import pickle

    with open(f'{wanted_file_name}.pkl','wb') as f:
        pickle.dump(file,f)


    # with open('omitted_routes.pkl', 'rb') as f:
    #     omitted_routes = pickle.load(f)
