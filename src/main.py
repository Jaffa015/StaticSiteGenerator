import os
import shutil

from copy_static import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
	print("Deleting public directory...")
	if os.path.isdir(dir_path_public):
		shutil.rmtree(dir_path_public)

	print("Copying static files to public directory")
	copy_files_recursive(dir_path_static, dir_path_public)


main()
