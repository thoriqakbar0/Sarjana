import sys
import os
import subprocess

from PySide6.QtWidgets import QApplication

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def build_extension():
  try:
      subprocess.check_call([sys.executable, 'setup.py', 'build_ext', '--inplace'])
      print("C extension built successfully.")
  except subprocess.CalledProcessError:
      print("Failed to build C extension.")
      sys.exit(1)

# Build the C extension
build_extension()

# Now import the C extension
from c_extensions import pdf_operations

from source.models.model_store import ModelStore
from source.services.services import Services
from source.views.main_window import MainWindow

def main():
  app = QApplication(sys.argv)
  
  # Initialize ModelStore and Services
  ModelStore()
  services = Services()

  # Create and show the main window
  window = MainWindow()
  window.show()
  
  sys.exit(app.exec())

if __name__ == "__main__":
  main()