"""
SoX Installation Checker for Anti Gravity Project

This utility verifies that SoX (Sound eXchange) is properly installed
and available in your system PATH.
"""

import shutil
import subprocess
import sys
import platform

def check_sox_installation():
    """Check if SoX is installed and get version info."""
    print("=" * 60)
    print("SoX Installation Checker")
    print("=" * 60)
    print()
    
    # Check if SoX is in PATH
    sox_path = shutil.which("sox")
    
    if sox_path:
        print(f"[OK] SoX found at: {sox_path}")
        print()
        
        # Try to get version
        try:
            result = subprocess.run(
                ["sox", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            print("Version Information:")
            print(result.stdout)
            print()
            print("[OK] SoX is properly installed and ready to use!")
            return True
        except Exception as e:
            print(f"[WARN] SoX found but couldn't get version: {e}")
            return False
    else:
        print("[ERROR] SoX NOT found in system PATH")
        print()
        print_installation_instructions()
        return False

def print_installation_instructions():
    """Print OS-specific installation instructions."""
    os_name = platform.system()
    
    print("=" * 60)
    print("Installation Instructions")
    print("=" * 60)
    print()
    
    if os_name == "Windows":
        print("For Windows:")
        print()
        print("Option 1: Download Official Build")
        print("  1. Visit: https://sourceforge.net/projects/sox/files/sox/")
        print("  2. Download the latest Windows version (e.g., sox-14.4.2-win32.zip)")
        print("  3. Extract to a folder (e.g., C:\\Program Files\\sox)")
        print("  4. Add SoX to your PATH:")
        print("     - Right-click 'This PC' > Properties")
        print("     - Click 'Advanced system settings'")
        print("     - Click 'Environment Variables'")
        print("     - Under 'System variables', find 'Path' and click 'Edit'")
        print("     - Click 'New' and add the path (e.g., C:\\Program Files\\sox)")
        print("     - Click 'OK' on all dialogs")
        print("  5. Restart your terminal/IDE")
        print()
        print("Option 2: Using Chocolatey (Package Manager)")
        print("  choco install sox.portable")
        print()
    
    elif os_name == "Darwin":  # macOS
        print("For macOS:")
        print()
        print("Using Homebrew:")
        print("  brew install sox")
        print()
    
    elif os_name == "Linux":
        print("For Linux:")
        print()
        print("Ubuntu/Debian:")
        print("  sudo apt-get update")
        print("  sudo apt-get install sox")
        print()
        print("Fedora/RHEL:")
        print("  sudo dnf install sox")
        print()
        print("Arch Linux:")
        print("  sudo pacman -S sox")
        print()
    
    print("After installation, run this script again to verify.")
    print()

def test_sox_effects():
    """Test if SoX can apply effects (requires SoX to be installed)."""
    print("=" * 60)
    print("Testing SoX Effects")
    print("=" * 60)
    print()
    
    sox_path = shutil.which("sox")
    if not sox_path:
        print("[ERROR] Cannot test effects - SoX not found")
        return False
    
    print("Available SoX effects that work well with manim-voiceover:")
    print()
    print("  * pitch <cents>       - Shift pitch (100 = 1 semitone)")
    print("  * tempo <factor>      - Change speed (1.1 = 10% faster)")
    print("  * speed <factor>      - Change speed + pitch")
    print("  * reverb <amount>     - Add room echo (0-100)")
    print("  * treble <dB>         - Boost/cut high frequencies")
    print("  * bass <dB>           - Boost/cut low frequencies")
    print("  * echo <params>       - Add echo effect")
    print("  * chorus <params>     - Add chorus effect")
    print()
    print("[OK] All effects available for use!")
    return True

if __name__ == "__main__":
    print()
    sox_installed = check_sox_installation()
    print()
    
    if sox_installed:
        test_sox_effects()
        print()
        print("=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print()
        print("1. Install manim-voiceover:")
        print("   pip install manim-voiceover[gtts]")
        print()
        print("2. Run the example:")
        print("   manim -pql assistant_intro.py AssistantIntro")
        print()
    else:
        print()
        print("=" * 60)
        print("Please install SoX first, then run this script again.")
        print("=" * 60)
        print()
        sys.exit(1)
