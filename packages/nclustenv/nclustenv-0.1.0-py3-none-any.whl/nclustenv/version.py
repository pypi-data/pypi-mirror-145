VERSION = '0.1.0'

ENV_LIST = [
    'BiclusterEnv-v0',
    'TriclusterEnv-v0',
    'OfflineBiclusterEnv-v0',
    'OfflineTriclusterEnv-v0'
]

TESTING_CONFIGS = [
    [
        {
            'shape': [[50, 10], [200, 50]],
            'n': 1,
            'clusters': [1, 3],
            'dataset_settings': {
                'patterns': dict(value=[
                    [['CONSTANT', 'CONSTANT'], ['Additive', 'Additive']],
                    [['Additive', 'Constant'], ['CONSTANT', 'CONSTANT']]
                ], type='categorical', randomize=True),
                'realval': dict(value=[True, False], type='categorical', randomize=True),
                'maxval': dict(value=11.0),
                'minval': dict(value=[-10.0, 1.0], type='continuous', randomize=True)
            },
            'max_steps': 150
        },
        {
            'shape': [[100, 10], [200, 50]],
            'n': None,
            'clusters': [1, 3],
        },
        {
            'shape': [[100, 10], [200, 50]],
            'n': 5,
            'clusters': [1, 5],
        }
    ],
    [
        {
            'shape': [[50, 10, 2], [200, 50, 4]],
            'n': 1,
            'clusters': [1, 3],
            'dataset_settings': {
                'patterns': dict(value=[
                    [['Constant', 'Constant', 'Constant'], ['Additive', 'Additive', 'Additive']],
                    [['Constant', 'Additive', 'Additive'], ['Constant', 'Constant', 'Constant']]
                ], type='categorical', randomize=True),
                'realval': dict(value=[True, False], type='categorical', randomize=True),
                'maxval': dict(value=11.0),
                'minval': dict(value=[-10.0, 1.0], type='continuous', randomize=True)
            },
            'max_steps': 150
        },
        {
            'shape': [[100, 10, 3], [200, 50, 5]],
            'n': None,
            'clusters': [1, 3],
        },
        {
            'shape': [[100, 10, 2], [200, 50, 3]],
            'n': 5,
            'clusters': [1, 5],
        }
    ],
    [
        {
            'n': 1,
            'max_steps': 150,
            'train_test_split': 0.8
        },
        {
            'n': None,
            'train_test_split': 0.1
        },
        {
            'n': 5,
            'train_test_split': 0.5
        },
    ],
    [
        {
            'n': 1,
            'max_steps': 150,
            'train_test_split': 0.8
        },
        {
            'n': None,
            'train_test_split': 0.1
        },
        {
            'n': 5,
            'train_test_split': 0.5
        },
    ],
]

TESTING_CONFIGS_DATASETS = [
    [
        {
            'name': 'test1',
            'length': 100,
            'shape': [[50, 10], [200, 50]],
            'clusters': [1, 3],
            'dataset_settings': {
                'patterns': dict(value=[
                    [['CONSTANT', 'CONSTANT'], ['Additive', 'Additive']],
                    [['Additive', 'Constant'], ['CONSTANT', 'CONSTANT']]
                ], type='categorical', randomize=True),
                'realval': dict(value=[True, False], type='categorical', randomize=True),
                'maxval': dict(value=11.0),
                'minval': dict(value=[-10.0, 1.0], type='continuous', randomize=True)
            },
            'seed': 4,
            'save_dir': 'test_files'

        },
        {
            'name': 'test2',
            'shape': [[100, 10], [200, 50]],
            'clusters': [1, 3],
            'seed': 4,
            'save_dir': 'test_files'

        },
        {
            'name': 'test3',
            'shape': [[100, 10], [200, 50]],
            'clusters': [1, 5],
            'seed': 4,
            'save_dir': 'test_files'
        }
    ],
    [
        {
            'name': 'test4',
            'length': 100,
            'shape': [[50, 10, 2], [200, 50, 4]],
            'clusters': [1, 3],
            'dataset_settings': {
                'patterns': dict(value=[
                    [['Constant', 'Constant', 'Constant'], ['Additive', 'Additive', 'Additive']],
                    [['Constant', 'Additive', 'Additive'], ['Constant', 'Constant', 'Constant']]
                ], type='categorical', randomize=True),
                'realval': dict(value=[True, False], type='categorical', randomize=True),
                'maxval': dict(value=11.0),
                'minval': dict(value=[-10.0, 1.0], type='continuous', randomize=True)
            },
            'seed': 4,
            'generator': 'TriclusterGenerator',
            'save_dir': 'test_files'
        },
        {
            'name': 'test5',
            'shape': [[100, 10, 3], [200, 50, 5]],
            'clusters': [1, 3],
            'seed': 4,
            'generator': 'TriclusterGenerator',
            'save_dir': 'test_files'
        },
        {
            'name': 'test6',
            'shape': [[100, 10, 2], [200, 50, 3]],
            'clusters': [1, 5],
            'seed': 4,
            'generator': 'TriclusterGenerator',
            'save_dir': 'test_files'
        }
    ],
]
