import unittest
import socket
import sys
from unittest.mock import patch, MagicMock
sys.path.append('../src')
from port_scanner_socket import scan_port, scan_subnet

class TestPortScanner(unittest.TestCase):
    
    @patch('socket.socket')
    def test_scan_port_open(self, mock_socket):
        # Setup mock for open port
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 0
        
        # Test scan_port with open port
        result = scan_port('192.168.1.1', 80)
        self.assertTrue(result)
        mock_socket_instance.settimeout.assert_called_with(0.1)
        mock_socket_instance.connect_ex.assert_called_with(('192.168.1.1', 80))
        mock_socket_instance.close.assert_called_once()
    
    @patch('socket.socket')
    def test_scan_port_closed(self, mock_socket):
        # Setup mock for closed port
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.return_value = 1
        
        # Test scan_port with closed port
        result = scan_port('192.168.1.1', 80)
        self.assertFalse(result)
        mock_socket_instance.settimeout.assert_called_with(0.1)
        mock_socket_instance.connect_ex.assert_called_with(('192.168.1.1', 80))
        mock_socket_instance.close.assert_called_once()
    
    @patch('socket.socket')
    def test_scan_port_error(self, mock_socket):
        # Setup mock for socket error
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect_ex.side_effect = socket.error
        
        # Test scan_port with socket error
        result = scan_port('192.168.1.1', 80)
        self.assertFalse(result)
        mock_socket_instance.settimeout.assert_called_with(0.1)
        mock_socket_instance.close.assert_called_once()
    
    @patch('port_scanner_socket.scan_port')
    def test_scan_subnet(self, mock_scan_port):
        # Setup mock for scan_port
        mock_scan_port.side_effect = [False, True, False]
        
        # Test scan_subnet
        result = scan_subnet('192.168.1.', 1, 1, 80, 82)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('192.168.1.1', 81))
        self.assertEqual(mock_scan_port.call_count, 3)

if __name__ == '__main__':
    unittest.main()
