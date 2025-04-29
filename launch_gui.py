import sys, os

# Headless environment check before importing anything else
def headless_check():
    if not os.environ.get('DISPLAY') or os.environ.get('FORCE_HEADLESS') == '1':
        print("No display found. GUI cannot be launched in a headless environment.")
        sys.stdout.flush()
        sys.exit(1)

headless_check()

# Only import GUI and run main() if not headless
def main():
    import GUI
    GUI.main()

if __name__ == "__main__":
    main()
