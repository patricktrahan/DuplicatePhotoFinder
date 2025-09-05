# 📷 Duplicate Photo Finder

Duplicate Photo Finder is a simple desktop app built with **Python** and **Tkinter** that scans a folder for duplicate image files using file hashing. It provides an easy-to-use interface to preview duplicates and delete unwanted files.

---

## ✨ Features
- Select a folder and scan for duplicate images
- Uses **MD5 hashing** to detect identical files
- Groups duplicate files together for review
- Preview images directly in the app
- Select specific files to delete with checkboxes
- Optionally keeps one file per group while deleting the rest
- Clean UI styled with **Tkinter ttk + PIL**

---

## 📸 Screenshots


---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/duplicate-photo-finder.git
   cd duplicate-photo-finder

2. Install the required dependencies:
   pip install pillow

3. Run the app:
python DuplicatePhotoFinder.py

🖥️ Usage

Launch the program.
Click Select Folder to choose the directory you want to scan.
Click Scan for Duplicates.
Select a duplicate group from the list to preview images.
Check the images you want to delete (or leave unchecked to keep the first one and delete the rest).
Click Delete Selected to clean up duplicates.

⚠️ Disclaimer
This tool now sends files to the recycle bin rather than permanently deleting.

🛠️ Tech Stack
Python 3
Tkinter (UI)
Pillow (PIL) (image handling)
hashlib (MD5 hashing for duplicate detection)