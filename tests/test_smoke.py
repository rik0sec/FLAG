import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1] / "ctf_quick_launcher.py"
sys.path.insert(0, str(APP.parent))
import ctf_quick_launcher as launcher


class SmokeTests(unittest.TestCase):
    def test_menu_exit(self):
        p = subprocess.run(
            [sys.executable, str(APP)], input="0\n", text=True,
            capture_output=True, timeout=5
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("RIK0SEC CTF QUICK LAUNCHER", p.stdout)
        self.assertIn("Terima kasih", p.stdout)

    def test_compiles(self):
        p = subprocess.run(
            [sys.executable, "-m", "py_compile", str(APP)],
            capture_output=True, text=True, timeout=5
        )
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_firewall_iptables_is_read_only(self):
        with patch("builtins.input", side_effect=["1"]), \
             patch.object(launcher.shutil, "which", return_value="/usr/sbin/iptables"), \
             patch.object(launcher, "run") as mocked_run:
            launcher.firewall()
        args = mocked_run.call_args.args[0]
        self.assertEqual(args, ["/usr/sbin/iptables", "-L", "-n", "-v", "--line-numbers"])

    def test_firewall_getfacl_accepts_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory, \
             patch("builtins.input", side_effect=["4", directory]), \
             patch.object(launcher.shutil, "which", return_value="/usr/bin/getfacl"), \
             patch.object(launcher, "run") as mocked_run:
            launcher.firewall()
        args = mocked_run.call_args.args[0]
        self.assertEqual(args, ["/usr/bin/getfacl", "-p", "--", str(Path(directory).resolve())])


if __name__ == "__main__":
    unittest.main()
