import os
import argparse
import time
import math

def estimate_space(num_files: int, file_size: int = 5, inode_overhead: int = 4096) -> int:
    """
    Estimate disk space required for file creation.

    Args:
        num_files (int): Number of files.
        file_size (int): Size of each file in bytes (default: 5).
        inode_overhead (int): Estimated overhead per file (default: 4096 bytes).

    Returns:
        int: Estimated total space in bytes.
    """
    return num_files * (file_size + inode_overhead)

def get_fs_stats(path: str):
    """
    Get free disk space and free inodes for the filesystem containing 'path'.
    Returns (free_bytes, free_inodes).
    """
    stats = os.statvfs(path)
    free_bytes = stats.f_bavail * stats.f_frsize
    free_inodes = stats.f_favail
    return free_bytes, free_inodes

def create_files(target_dir: str, num_files: int, subdirs: int = 256, file_size: int = 5) -> None:
    """
    Create a specified number of files, distributed across subdirectories.

    Args:
        target_dir (str): The root directory for file creation.
        num_files (int): The number of files to create.
        subdirs (int): Number of subdirectories per level (default: 256).
        file_size (int): Size of each file in bytes (default: 5).
    """
    files_per_dir = math.ceil(num_files / (subdirs * subdirs))
    total_dirs = subdirs * subdirs
    est_space = estimate_space(num_files, file_size)
    free_bytes, free_inodes = get_fs_stats(target_dir if os.path.exists(target_dir) else os.path.dirname(target_dir))

    print("Summary:")
    print(f"- Target directory: {target_dir}")
    print(f"- Number of files: {num_files}")
    print(f"- Subdirectories per level: {subdirs}")
    print(f"- Total subdirectories (2 levels): {total_dirs}")
    print(f"- Files per leaf directory (approx): {files_per_dir}")
    print(f"- Estimated disk space required: {est_space / (1024*1024):.2f} MB")
    print(f"- Free disk space: {free_bytes / (1024*1024):.2f} MB")
    print(f"- Free inodes: {free_inodes}")
    print(f"- Example cleanup command: rm -rf {os.path.join(target_dir, '[0-9a-f][0-9a-f]')}")
    if est_space > free_bytes:
        print("WARNING: Estimated required disk space exceeds available space!")
    if num_files > free_inodes:
        print("WARNING: Estimated required inodes exceeds available inodes!")
    if os.path.exists(target_dir) and os.listdir(target_dir):
        print("WARNING: Target directory already exists and is not empty.")
    print("WARNING: Creating many files may impact system performance.\n")

    confirm = input("Proceed? (y/N): ").strip().lower()
    if confirm != "y":
        print("Aborted by user.")
        return

    start_time = time.time()
    created = 0
    for i in range(num_files):
        level1 = f"{(i // subdirs) % subdirs:02x}"
        level2 = f"{i % subdirs:02x}"
        dir_path = os.path.join(target_dir, level1, level2)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"testfile_{i}")
        try:
            with open(file_path, "w") as file:
                file.write("x" * file_size)
            created += 1
            if created % 1000 == 0:
                print(f"Created {created} files...")
        except Exception as error:
            print(f"Stopped at {created} files due to error: {error}")
            break
    elapsed = time.time() - start_time
    print("\nFile creation complete.")
    print(f"Total files created: {created}")
    print(f"Elapsed time: {elapsed:.2f} seconds")

def main() -> None:
    """
    Parse command-line arguments and initiate file creation.
    """
    parser = argparse.ArgumentParser(
        description="Create many files, distributed across subdirectories, to test filesystem limits."
    )
    parser.add_argument("target_dir", help="Root directory to create files in.")
    parser.add_argument("num_files", type=int, help="Number of files to create.")
    parser.add_argument("--subdirs", type=int, default=256, help="Subdirectories per level (default: 256).")
    parser.add_argument("--file-size", type=int, default=5, help="Size of each file in bytes (default: 5).")
    args = parser.parse_args()
    create_files(args.target_dir, args.num_files, args.subdirs, args.file_size)

if __name__ == "__main__":
    main()