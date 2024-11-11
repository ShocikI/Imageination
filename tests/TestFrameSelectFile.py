import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest import TestCase
from unittest.mock import patch, MagicMock
import tkinter
from PIL import Image

from source.data.SystemData import SystemData

class TestFrameSelectFile(TestCase):
    mock_data: SystemData
    
    @classmethod
    def setup_class(cls):
        cls.mock_data = SystemData()
        # Mock file_list as Combobox
        cls.mock_data.file_list = MagicMock()
        cls.mock_data.file_list.configure_mock(**{'values': []})
        # Mock mean_tree as Treeview
        cls.mock_data.mean_tree = MagicMock()
        cls.mock_data.mean_tree.get_children.return_value = []
        cls.mock_data.mean_tree.insert = MagicMock()
    
    @classmethod
    def teardown_class(cls):
        del cls.mock_ata

    @patch('PIL.Image.open')
    @patch('tkinter.filedialog.askopenfilenames')
    def test_select_files_works(self, mock_filedialog, mock_images):
        # Mocks
        return_path = ('path/to/first.png', 'path/to/second.png')
        mock_filedialog.return_value = return_path
        mock_images.return_value = Image.new('RGB', (684, 741), color=(255, 255, 255))

        # Call function
        self.mock_data.select_files()

        # Check file_names
        self.assertEqual(2, len(self.mock_data.file_names))
        self.assertEqual(list(return_path), self.mock_data.file_names)
        # Check mean_data
        self.assertIn('path/to/first.png', self.mock_data.mean_data)
        self.assertIn('path/to/second.png', self.mock_data.mean_data)
        self.assertEqual(self.mock_data.mean_data['path/to/first.png'], { "weight": 1, "height": 741, "width": 684, "mode": 'RGB' })

        # Reset values
        self.mock_data.file_names = []
        self.mock_data.file_list.configure_mock(**{'values': []})

    @patch('tkinter.filedialog.askopenfilenames')
    def test_select_files_empty_path(self, mock_filedialog):
        # Mocks
        mock_filedialog.return_value = ''

        # Call function
        self.mock_data.select_files()
        # Check file_names
        self.assertEqual(0, len(self.mock_data.file_names))
        self.assertEqual([], self.mock_data.file_names)

    @patch('PIL.Image.open')
    @patch('os.listdir')
    @patch('os.chdir')
    @patch('tkinter.filedialog.askdirectory')
    def test_select_folder_works(self, mock_filedialog, mock_chdir, mock_listdir, mock_images):
        # Mocks
        folder_path = 'path\\to\\folder'
        mock_filedialog.return_value = folder_path
        mock_chdir.return_value = None
        mock_listdir.return_value = ('first.png', 'second.png', 'error.txt')
        mock_images.return_value = Image.new('RGB', (684, 741), color=(255, 255, 255))

        # Call function
        self.mock_data.select_folder()
        # Imitate result paths
        result = [os.path.join( folder_path, path) for path in ['first.png', 'second.png']]
        # Check file_names 
        # 2 files added now and 2 earlier
        self.assertEqual(2, len(self.mock_data.file_names))
        self.assertEqual(result, self.mock_data.file_names)
        
        # Reset values
        self.mock_data.file_names = []
        self.mock_data.file_list.configure_mock(**{'values': []})

    @patch('os.chdir')
    @patch('tkinter.filedialog.askdirectory')
    def test_select_folder_empty_path(self, mock_filedialog, mock_chdir):
        # Mocks
        folder_path = ''
        mock_filedialog.return_value = folder_path
        mock_chdir.return_value = None
        
        # Call function
        self.mock_data.select_folder()
        # Check file_names 

        # 2 files added now and 2 earlier
        self.assertEqual(0, len(self.mock_data.file_names))
        self.assertEqual([], self.mock_data.file_names)

    def test_remove_file(self):
        # Init values
        self.mock_data.file_names = ['path/to/first.png', 'path/to/second.png']
        for file in self.mock_data.file_names:
            self.mock_data.mean_data[file] = { "weight": 1,  "height": 500, "width": 500, "mode": "RGB" }
        # Check if values are ready
        self.assertEqual(2, len(self.mock_data.file_names))
        self.assertIn('path/to/first.png', self.mock_data.mean_data)
        self.assertEqual(self.mock_data.mean_data['path/to/first.png'], { "weight": 1,  "height": 500, "width": 500, "mode": "RGB" })
        self.assertIn('path/to/second.png', self.mock_data.mean_data)
        self.assertEqual(self.mock_data.mean_data['path/to/first.png'], { "weight": 1,  "height": 500, "width": 500, "mode": "RGB" })
        # Remove one by one elements
        for i in reversed(range(len(self.mock_data.file_names))):
            self.mock_data.remove_file(self.mock_data.file_names[i])
            self.assertEqual(i, len(self.mock_data.file_names))
        # Final check
        self.assertEqual(0, len(self.mock_data.file_names))
        self.assertEqual([], self.mock_data.file_names)
        self.assertNotIn('path/to/first.png', self.mock_data.mean_data)
        self.assertNotIn('path/to/second.png', self.mock_data.mean_data)
        
        # Reset values
        self.mock_data.file_names = []
        self.mock_data.file_list.configure_mock(**{'values': []})

    def test_remove_selected_in_select_file_combobox(self):
        # Set file_list.get()
        self.mock_data.file_list.get.return_value = 'path/to/first.png'
        
        # Init values
        self.mock_data.file_names = ['path/to/first.png', 'path/to/second.png']
        self.mock_data.mean_data = {
            'path/to/first.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'},
            'path/to/second.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'}
        }
        
        # Call function
        self.mock_data.remove_selected_in_select_file_combobox()
        
        # Check file_names and mean_data
        self.assertNotIn('path/to/first.png', self.mock_data.file_names)
        self.assertNotIn('path/to/first.png', self.mock_data.mean_data)
        
        # Reset values
        self.mock_data.file_names = []
        self.mock_data.file_list.configure_mock(**{'values': []})

    def test_remove_selected_in_mean_image_tree(self):
        # Set mean_tree.selection()
        self.mock_data.mean_tree.selection.return_value = ['item1', 'item2']
        # Set mean_tree.item()
        self.mock_data.mean_tree.item.side_effect = lambda item: {'values': ['path/to/first.png'] if item == 'item1' else ['path/to/second.png']}
        
        # Dodanie przykładowych danych do file_names i mean_data
        self.mock_data.file_names = ['path/to/first.png', 'path/to/second.png']
        self.mock_data.mean_data = {
            'path/to/first.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'},
            'path/to/second.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'}
        }
        
        # Wywołanie funkcji
        self.mock_data.remove_selected_in_mean_image_tree()
        
        # Sprawdzenie, czy pliki zostały usunięte
        self.assertNotIn('path/to/first.png', self.mock_data.file_names)
        self.assertNotIn('path/to/second.png', self.mock_data.file_names)
        self.assertNotIn('path/to/first.png', self.mock_data.mean_data)
        self.assertNotIn('path/to/second.png', self.mock_data.mean_data)
        
        # Reset values
        self.mock_data.file_names = []
        self.mock_data.file_list.configure_mock(**{'values': []})

    def test_clear_selection(self):
        # Init values
        self.mock_data.file_names = ['path/to/first.png', 'path/to/second.png']
        self.mock_data.mean_data = {
            'path/to/first.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'},
            'path/to/second.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'}
        }
        
        # Call function
        self.mock_data.clear_selection()
        
        # Final check
        self.assertEqual(self.mock_data.file_names, [])
        self.assertEqual(self.mock_data.mean_data, {})

    
    def test_update_files_data_empty(self):
        # Init values
        self.mock_data.file_names = []
        self.mock_data.mean_data = {}
        
        # Mock get_children
        self.mock_data.mean_tree.get_children.return_value = []
        
        # Call function
        self.mock_data.update_files_data()
        
        self.mock_data.file_list.set.assert_called_with("")
        
        # Final check
        self.mock_data.mean_tree.delete.assert_not_called()

    def test_update_files_data_with_data(self):
        # Init values
        self.mock_data.file_names = ['path/to/first.png', 'path/to/second.png']
        self.mock_data.mean_data = {
            'path/to/first.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'},
            'path/to/second.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'}
        }
        # Mock get_children
        self.mock_data.mean_tree.get_children.return_value = {'path/to/first.png': {'weight': 1, 'height': 600, 'width': 800, 'mode': 'RGB'},}

        # Call function
        self.mock_data.update_files_data()
        
        # Check if values are updated
        self.mock_data.file_list.__setitem__.assert_called_with('values', self.mock_data.file_names)
        self.mock_data.file_list.set.assert_called_with("")
        
        # Check if mean_tree is cleared
        self.mock_data.mean_tree.delete.assert_called()
        
        # Check if mean_tree are updated
        self.mock_data.mean_tree.insert.assert_any_call("", 'end', values=('path/to/first.png', 1, 600, 800, 'RGB'))
        self.mock_data.mean_tree.insert.assert_any_call("", 'end', values=('path/to/second.png', 1, 600, 800, 'RGB'))
