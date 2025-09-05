
<h1>📷 Duplicate Photo Finder</h1>

<h3>Duplicate Photo Finder is a simple desktop app built with **Python** and **Tkinter** that scans a folder for duplicate image files using file hashing. It provides an easy-to-use interface to preview duplicates and delete unwanted files.</h2>

<h2>✨ Features</h2>
   <ul>
      <li>Select a folder and scan for duplicate images</li>
      <li>Uses **MD5 hashing** to detect identical files</li>
      <li>Groups duplicate files together for review</li>
      <li>Preview images directly in the app</li>
      <li>Select specific files to delete with checkboxes</li>
      <li>Optionally keeps one file per group while deleting the rest</li>
      <li>Clean UI styled with **Tkinter ttk + PIL**</li>
   </ul>

<h2>📸 Screenshots</h2>

<h2>🖥️ Usage</h2>
   <ul>
      <li>Launch the program.</li>
      <li>Click Select Folder to choose the directory you want to scan.</li>
      <li>Click Scan for Duplicates.</li>
      <li>Select a duplicate group from the list to preview images.</li>
      <li>Check the images you want to delete (or leave unchecked to keep the first one and delete the rest).</li>
      <li>Click Delete Selected to clean up duplicates.</li>
   </ul>

<h2>⚠️ Disclaimer</h2>
   <p>This tool now sends files to the recycle bin rather than permanently deleting.</p>

<h2>🛠️ Tech Stack</h2>
   <ul>
      <li>Python 3</li>
      <li>Tkinter (UI)</li>
      <li>Pillow (PIL) (image handling)</li>
      <li>hashlib (MD5 hashing for duplicate detection)</li>
   </ul>
