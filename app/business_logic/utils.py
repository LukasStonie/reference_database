import os


def remove_spectrum(file_path):
    """
        Removes a spectrum (csv and png file) from the filesystem.

    Args:
        file_path (string): path to the csv file that should be deleted.

    Returns:
        None
    """
    os.remove(file_path)  # remove csv
    os.remove(file_path.replace('.csv', '.png'))  # remove plot
