#!/usr/bin/env python
"""
Functionality and script to upload data to the [Brevetti AI Platform](https://platform.brevetti.ai)

"""
import argparse
import os.path
import time
import concurrent
from tqdm import tqdm
import os
from brevettiai.platform.models.dataset import Dataset
from brevettiai.platform import PlatformAPI


def recursive_relative_paths(path):
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            dataset_path = os.path.relpath(file_path, path)
            yield (file_path, dataset_path.replace("\\", "/"))


def copy_recursive(dataset, folder_path, exlude=None, include=None):
    def upload_to_ds(ds, src, ds_target):
        pth = ds.get_location(ds_target)

        status = ds.io.copy(src, pth)
        return pth

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = []
        for (disk_path, dataset_path) in recursive_relative_paths(folder_path):
            future = executor.submit(upload_to_ds,
                                    dataset, disk_path, dataset_path)
            futures.append(future)
    for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        pass


"""
Example usage:

python -m brevettiai.utils.upload_data my_local_folder --dataset_name "My new dataset name" --username my_name@my_domain.com --password *****
"""
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', help='Absolute path to the folder containing the Dataset')
    parser.add_argument('--dataset_name', help='Name of the dataset as it will appear on the platform')
    parser.add_argument('--reference', help='Reference Field for the dataset')
    parser.add_argument('--username', help='Brevetti-AI platform username (https://platform.brevetti.ai)')
    parser.add_argument('--password', help='Brevetti-AI platform password (https://platform.brevetti.ai)')
    parser.add_argument('--dataset_id', help="Id of existing dataset to upload to")

    args = parser.parse_args()

    platform = PlatformAPI(args.username, args.password)

    if args.dataset_id:
        dataset = platform.get_dataset(args.dataset_id, write_access=True)
    else:
        ds_name = args.dataset_name if args.dataset_name else os.path.basename(args.input_folder)
        dataset = Dataset(name=ds_name, reference=args.reference)
        print(f'Creating dataset {ds_name} on platform')
        dataset = platform.create(dataset, write_access=True)


    start_procedure = time.time()

    print('Copy entire dataset to s3...')

    copy_recursive(dataset, args.input_folder)  # , exclude=args.exclude)

    print('End copy...')
    print(f'Dataset Created-Posted in {time.time() - start_procedure}s...')
