import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest import TestCase
from unittest.mock import patch, MagicMock
from tkinter import Listbox, colorchooser
from PIL import Image
import numpy as np

from source.data.SystemData import SystemData
from source.data.SwitchData import SwitchData
import source.ops.FrameSwitchColorOperators as ops

class TestColorSwitching(TestCase):
    @patch('tkinter.colorchooser.askcolor')
    def test_select_target_color(self, mock_color):
        # Simulate color selection
        mock_item = MagicMock(spec=SwitchData)
        mock_item.color_list = []
        mock_item.box_switches = MagicMock(spec=Listbox)

        # Simulate selecting a color
        mock_color.return_value = ((255, 0, 0), '#ff0000')
        ops.select_target_color(mock_item)
        # Test that the color was added to the color list and box switches
        self.assertIn(mock_color.return_value[0], mock_item.color_list)
        mock_item.box_switches.insert.assert_called_once_with(len(mock_item.color_list)+1, mock_color.return_value[1])

    def test_remove_selected_color(self):
        # Mock the Listbox to simulate a selection
        mock_item = MagicMock(spec=SwitchData)
        mock_item.box_switches = MagicMock(spec=Listbox)
        mock_item.box_switches.curselection.return_value = (0,)

        # Add some items to the list
        mock_item.box_switches.get = MagicMock(return_value=["#ff0000"])

        # Simulate removing a selected color
        ops.remove_selected_color(mock_item)

        # Ensure that the selected color was removed
        mock_item.box_switches.delete.assert_called_once_with((0, ))

    def test_generate_images_validation_without_files(self):
        # Test case where validation fails if no image is selected
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = []
        mock_data.switch_data = [MagicMock(spec=SwitchData)]
        
        with patch('tkinter.messagebox.showinfo') as mock_message:
            result = ops.validate_data(mock_data)
            self.assertTrue(result)  # Should return True indicating validation failure
            mock_message.assert_called_with(message='Select 1 image in "File selection".')

    def test_generate_images_validation_without_data(self):
        # Test case where validation fails if no image is selected
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = ["path\\to\\first.png"]
        mock_data.switch_data = []
        print(len(mock_data.switch_data))
        with patch('tkinter.messagebox.showinfo') as mock_message:
            result = ops.validate_data(mock_data)
            self.assertTrue(result)  # Should return True indicating validation failure
            mock_message.assert_called_with(message='Select at least 1 color to switch.')

    @patch('tkinter.filedialog.askdirectory')
    def test_generate_images_validation(self, mock_color):
        # Test case where validation fails if no image is selected
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = []
        mock_data.switch_data = [MagicMock(spec=SwitchData)]
        
        with patch('tkinter.messagebox.showinfo') as mock_message:
            result = ops.validate_data(mock_data)
            self.assertTrue(result)  # Should return True indicating validation failure
            mock_message.assert_called_with(message='Select 1 image in "File selection".')

            
    def test_make_look_up_table(self):
        # Test case where we create a lookup table with cubic tolerance
        mock_matrix = np.array([
            [[100, 150, 200], [100, 150, 200]], 
            [[50, 50, 50], [200, 200, 200]]
        ])
        mock_switch_data = [
            MagicMock(spec=SwitchData, rgb_color=(100, 150, 200), hex_color='#6496C8', use_tolerance=False, keep_difference=False)
        ]

        table = ops.make_look_up_table(mock_matrix, mock_switch_data)

        # Test that a lookup table is generated for the specified color
        self.assertIn('#6496C8', table)
        self.assertEqual(
            table['#6496C8'], 
            [(0, 0, False, 0, 0, 0), (0, 1, False, 0, 0, 0)]
        )


    @patch("tkinter.filedialog.askdirectory")
    @patch("PIL.Image.open")
    @patch("source.ops.FrameSwitchColorOperators.make_look_up_table")
    @patch("source.ops.FrameSwitchColorOperators.generate_file")
    def test_generate_images_with_valid_data(self, mock_generate_file, mock_make_look_up_table, mock_image_open, mock_askdirectory):
        # Mock configurations
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = []
        mock_data.switch_data = []
        mock_image_open.return_value = MagicMock()
        mock_askdirectory.return_value = "/fake/directory"
        mock_make_look_up_table.return_value = {}

        # Create sample SwitchData instances
        switch_data_1 = SwitchData(parent=None, remove_callback=None, rgb=(255, 255, 255), hex="#FF0000")
        switch_data_1.color_list = ["#FF0000"]
        switch_data_2 = SwitchData(parent=None, remove_callback=None, rgb=(0, 0, 0), hex="#00FF00")
        switch_data_2.color_list = ["#00FF00"]

        # Run the function
        self.assertEqual(len(mock_data.switch_data), 0)
        ops.generate_images(mock_data)
        self.assertEqual(len(mock_data.switch_data), 0)
        self.assertEqual(mock_data.file_names, [])


    @patch("tkinter.filedialog.askdirectory", return_value="")
    def test_directory_not_selected(self, mock_askdirectory):
        # Create sample data
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = ["test_image.jpg"]
        mock_data.switch_data = []
        mock_askdirectory.return_value = ""
        switch_data_1 = SwitchData(parent=None, remove_callback=None, rgb=(255, 255, 255), hex="#FF0000")
        switch_data_1.color_list = ["#FF0000"]  # Target color to switch to

        # Call function
        result = ops.generate_images(mock_data)
        
        # Check if function exits early when no directory is selected
        self.assertIsNone(result)


    @patch("source.ops.FrameSwitchColorOperators.validate_data", return_value=True)
    def test_invalid_data_returns_none(self, mock_validate_data):
        # Create sample data
        mock_data = MagicMock(spec=SystemData)
        mock_data.file_names = ["test_image.jpg"]
        mock_data.switch_data = []
        switch_data_1 = SwitchData(parent=None, remove_callback=None, rgb=(255, 255, 255), hex="#FF0000")
        switch_data_1.color_list = ["#FF0000"]  # Target color to switch to

        # Call function
        result = ops.generate_images(mock_data)

        # Ensure function returned None due to invalid data
        self.assertIsNone(result)
        mock_validate_data.assert_called_once_with(mock_data)