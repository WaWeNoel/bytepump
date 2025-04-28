import os
import random
import shutil
import threading
import multiprocessing
import platform
import psutil
from concurrent.futures import ThreadPoolExecutor

class TextColors:
    YELLOW_BLACK = '\033[43m\033[30m'
    ORANGE = '\033[33m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_RED = '\033[41m'
    ENDC = '\033[0m'

class PerformanceMode:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    AGGRESSIVE = 4

def print_logo():
    logo = f"""
    {TextColors.CYAN}
 _           _                                   
| |         | |                                  
| |__  _   _| |_ ___ _ __  _   _ _ __ ___  _ __  
| '_ \| | | | __/ _ \ '_ \| | | | '_ ` _ \| '_ \ 
| |_) | |_| | ||  __/ |_) | |_| | | | | | | |_) |
|_.__/ \__, |\__\___| .__/ \__,_|_| |_| |_| .__/ 
        __/ |       | |                   | |    
       |___/        |_|                   |_|    

              
  
  {TextColors.BACKGROUND_GREEN}Welcome to Multi-mode File Pumper!{TextColors.ENDC}
  --------------------------------
  Version: {TextColors.CYAN}1.0.0{TextColors.ENDC}
  By: {TextColors.CYAN}WaWeNoel{TextColors.ENDC}
  Github: {TextColors.CYAN}https://github.com/WaWeNoel/{TextColors.ENDC}
"""
    print(logo)

def print_performance_modes():
    print(f"\n{TextColors.CYAN}=== Performance Modes ==={TextColors.ENDC}")
    print(f"{TextColors.ORANGE}1. Low (Safe mode):")
    print("   - Single thread")
    print("   - 64KB chunks")
    print("   - CPU-friendly")
    print("   - Recommended for weak systems")
    
    print(f"\n2. Medium (Balanced):")
    print("   - 4 threads max")
    print("   - 1MB chunks")
    print("   - Good for most systems")
    
    print(f"\n3. High (Performance):")
    print("   - 8 threads max")
    print("   - 10MB chunks")
    print("   - Fast operation")
    
    print(f"\n4. Aggressive (Max power):")
    print(f"   - All CPU threads ({multiprocessing.cpu_count()} threads)")
    print("   - 100MB chunks")
    print("   - Maximum speed")
    print("   - May cause system strain")
    print(f"{TextColors.CYAN}========================={TextColors.ENDC}")

def print_pump_modes():
    print(f"\n{TextColors.CYAN}=== Pumping Modes ==={TextColors.ENDC}")
    print(f"{TextColors.ORANGE}1. Text files (.txt, .log, .csv)")
    print("   - Adds text headers with random data")
    
    print(f"\n2. Media files (.mp3, .mp4, .jpg)")
    print("   - Appends random binary data")
    
    print(f"\n3. Archives (.zip, .rar, .7z)")
    print("   - Adds null bytes with archive headers")
    
    print(f"\n4. Executables (.exe, .dll)")
    print("   - Adds executable-safe padding")
    
    print(f"\n5-17. Specialized modes:")
    print("   - PDF, Office docs, Databases etc.")
    
    print(f"\n99. Ultra-fast mode:")
    print("   - Maximum speed with random data")
    print("   - Performance scales with selected mode")
    print(f"{TextColors.CYAN}===================={TextColors.ENDC}")

class SystemSpecs:
    def __init__(self):
        self.cpu_cores = multiprocessing.cpu_count()
        self.cpu_freq = psutil.cpu_freq().max / 1000 if psutil.cpu_freq() else 2.5
        self.ram = psutil.virtual_memory().total / (1024 ** 3)
        self.disk_type = self._detect_disk_type()
        self.is_laptop = self._check_if_laptop()
    
    def _detect_disk_type(self):
        try:
            if platform.system() == 'Linux':
                with open('/sys/block/sda/queue/rotational') as f:
                    return 'SSD' if f.read().strip() == '0' else 'HDD'
            elif platform.system() == 'Windows':
                return 'SSD' if 'SSD' in os.popen('wmic diskdrive get MediaType').read() else 'HDD'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def _check_if_laptop(self):
        if platform.system() == 'Linux':
            return os.path.exists('/sys/class/power_supply/BAT0')
        elif platform.system() == 'Windows':
            return 'Portable' in os.popen('wmic computersystem get PCSystemType').read()
        else:
            return False

def analyze_system():
    specs = SystemSpecs()
    score = 0
    score += min(40, specs.cpu_cores * 5 + specs.cpu_freq * 2)
    score += min(30, specs.ram * 5)
    if specs.disk_type == 'SSD':
        score += 20
    elif specs.disk_type == 'HDD':
        score += 5
    if specs.is_laptop:
        score -= 10
    
    if score < 30:
        return PerformanceMode.LOW, specs
    elif score < 60:
        return PerformanceMode.MEDIUM, specs
    elif score < 90:
        return PerformanceMode.HIGH, specs
    else:
        return PerformanceMode.AGGRESSIVE, specs

current_performance_mode = PerformanceMode.MEDIUM
system_specs = SystemSpecs()
MAX_THREADS = system_specs.cpu_cores

def print_system_info(specs):
    print(f"\n{TextColors.CYAN}=== System Analysis ==={TextColors.ENDC}")
    print(f"CPU Cores: {specs.cpu_cores} @ {specs.cpu_freq:.1f}GHz")
    print(f"RAM: {specs.ram:.1f}GB")
    print(f"Storage: {specs.disk_type}")
    print(f"Laptop: {'Yes' if specs.is_laptop else 'No'}")
    print(f"{TextColors.CYAN}====================={TextColors.ENDC}\n")

def set_performance_mode(mode, specs=None):
    global current_performance_mode
    current_performance_mode = mode
    modes = {
        1: "LOW (Safe mode)",
        2: "MEDIUM (Balanced)",
        3: "HIGH (Performance)",
        4: f"AGGRESSIVE (Max power, {MAX_THREADS} threads)"
    }
    print(f"\n{TextColors.BACKGROUND_GREEN}Selected performance: {modes[mode]}{TextColors.ENDC}")
    if specs:
        print(f"{TextColors.CYAN}Recommended for your system{TextColors.ENDC}")

def auto_detect_mode():
    try:
        recommended_mode, specs = analyze_system()
        print_system_info(specs)
        print(f"\n{TextColors.BACKGROUND_GREEN}Recommended mode: {recommended_mode}{TextColors.ENDC}")
        print("1. Accept recommendation")
        print("2. Choose manually")
        choice = input("Selection: ")
        if choice == '1':
            set_performance_mode(recommended_mode, specs)
            return recommended_mode
    except Exception as e:
        print(f"{TextColors.RED}Auto-detection failed: {e}{TextColors.ENDC}")
    
    print_performance_modes()
    while True:
        try:
            mode = int(input("\nSelect performance mode (1-4): "))
            if 1 <= mode <= 4:
                set_performance_mode(mode)
                return mode
            print("Invalid choice")
        except ValueError:
            print("Enter a number")

def get_chunk_size(total_size):
    if current_performance_mode == PerformanceMode.LOW:
        return min(1024 * 64, total_size)  # 64KB chunks
    elif current_performance_mode == PerformanceMode.MEDIUM:
        return min(1024 * 1024, total_size)  # 1MB chunks
    elif current_performance_mode == PerformanceMode.HIGH:
        return min(1024 * 1024 * 10, total_size)  # 10MB chunks
    else:  # AGGRESSIVE
        return min(1024 * 1024 * 100, total_size)  # 100MB chunks

def get_thread_count():
    if current_performance_mode == PerformanceMode.LOW:
        return 1
    elif current_performance_mode == PerformanceMode.MEDIUM:
        return min(4, MAX_THREADS)
    elif current_performance_mode == PerformanceMode.HIGH:
        return min(8, MAX_THREADS)
    else:  # AGGRESSIVE
        return MAX_THREADS

def validate_file_path(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"{TextColors.YELLOW_BLACK}Error: The specified file '{file}' does not exist.{TextColors.ENDC}")

def validate_file_size(file_size):
    suffix = file_size[-2:].lower()
    if suffix not in ['kb', 'mb', 'gb']:
        raise ValueError(f"{TextColors.RED}Invalid format.{TextColors.ORANGE} Use 'KB', 'MB', or 'GB'.{TextColors.ENDC}")
    if not file_size[:-2].isdigit():
        raise ValueError(f"{TextColors.RED}Invalid value.{TextColors.ORANGE} Use numeric values.{TextColors.ENDC}")
    
    numeric = int(file_size[:-2])
    if suffix == 'gb' and numeric > 100:
        raise ValueError(f"{TextColors.BACKGROUND_RED}File size too large! 100GB+ not allowed.{TextColors.ENDC}")
    if suffix == 'gb' and numeric > 10:
        print(f"{TextColors.YELLOW_BLACK}Warning: You are about to add more than 10GB to a file!{TextColors.ENDC}")
    if suffix == 'mb' and numeric > 1024 * 5:
        print(f"{TextColors.YELLOW_BLACK}Warning: That's more than 5GB. Proceed with caution.{TextColors.ENDC}")

def check_writable(file):
    if not os.access(file, os.W_OK):
        raise PermissionError(f"{TextColors.BACKGROUND_RED}File is not writable!{TextColors.ENDC}")

def check_disk_space(file, needed_bytes):
    stat = shutil.disk_usage(os.path.dirname(os.path.abspath(file)))
    if stat.free < needed_bytes:
        raise OSError(f"{TextColors.BACKGROUND_RED}Not enough free space! Needed: {needed_bytes}, Available: {stat.free}{TextColors.ENDC}")

def confirm_large_addition(size_bytes):
    if size_bytes > 1024 * 1024 * 1024 * 5:  # 5GB
        answer = input(f"{TextColors.YELLOW_BLACK}You are about to write more than 5GB. Are you sure? (y/n): {TextColors.ENDC}")
        if answer.lower() != 'y':
            raise KeyboardInterrupt(f"{TextColors.RED}Operation cancelled by user.{TextColors.ENDC}")

def parse_size(size):
    unit = size[-2:].lower()
    num = int(size[:-2])
    if unit == 'kb': return num * 1024
    if unit == 'mb': return num * 1024 * 1024
    if unit == 'gb': return num * 1024 * 1024 * 1024

def get_extension_mode(file):
    ext = os.path.splitext(file)[1].lower()
    return {
        '.txt': 1, '.log': 1, '.csv': 1, '.md': 14,
        '.mp3': 2, '.mp4': 2, '.avi': 2, '.mkv': 2, '.flac': 2,
        '.jpg': 2, '.jpeg': 2, '.png': 2, '.gif': 2, '.bmp': 2,
        '.wav': 2, '.webm': 2, '.mov': 2,
        '.zip': 3, '.rar': 3, '.7z': 3, '.tar': 3, '.gz': 3, '.bz2': 3, '.xz': 3,
        '.exe': 4, '.dll': 4, '.bin': 4, '.elf': 4, '.apk': 4, '.iso': 4,
        '.json': 7, '.xml': 7, '.yml': 7, '.yaml': 7,
        '.db': 8, '.sqlite': 8, '.sql': 8,
        '.pdf': 9,
        '.html': 10, '.htm': 10, '.css': 10, '.js': 10,
        '.docx': 11, '.xlsx': 11, '.pptx': 11, '.odt': 11, '.ods': 11, '.odp': 11,
        '.torrent': 12,
        '.ttf': 13, '.otf': 13, '.woff': 13, '.woff2': 13,
        '.sh': 15, '.bash': 15, '.zsh': 15,
        '.epub': 16,
        '.sqlite3': 17, '.db3': 17,
        '.fast': 99
    }.get(ext, 6)

def pump_file_segment(file, start_pos, size, mode_func):
    with open(file, 'r+b') as f:
        f.seek(start_pos)
        mode_func(f, size)

def threaded_pump(file, size, mode_func):
    if current_performance_mode == PerformanceMode.LOW:
        with open(file, 'ab') as f:
            mode_func(f, size)
        return
    
    thread_count = get_thread_count()
    chunk_size = get_chunk_size(size // thread_count)
    
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        remaining = size
        position = os.path.getsize(file)
        
        while remaining > 0:
            current_chunk = min(chunk_size, remaining)
            futures.append(executor.submit(pump_file_segment, file, position, current_chunk, mode_func))
            position += current_chunk
            remaining -= current_chunk
        
        for future in futures:
            future.result()

def pump_mode_1(file, size):
    def mode_func(f, chunk_size):
        if f.tell() == 0:
            f.write(b"\n# PADDING START\n")
            chunk_size -= len(b"\n# PADDING START\n")
        f.write(os.urandom(chunk_size))
    
    threaded_pump(file, size, mode_func)
    print(f"{TextColors.BACKGROUND_GREEN}Mode 1: Text-based file padded.{TextColors.ENDC}")

def pump_mode_2(file, size):
    threaded_pump(file, size, lambda f, chunk: f.write(os.urandom(chunk)))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 2: Media file padded.{TextColors.ENDC}")

def pump_mode_3(file, size):
    threaded_pump(file, size, lambda f, chunk: f.write(b"\x00" * chunk))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 3: Archive padded.{TextColors.ENDC}")

def pump_mode_4(file, size):
    def mode_func(f, chunk_size):
        if f.tell() == 0:
            f.write(b'\x50\x4B\x05\x06')
            chunk_size -= 4
        f.write(b'\x00' * chunk_size)
    
    threaded_pump(file, size, mode_func)
    print(f"{TextColors.BACKGROUND_GREEN}Mode 4: EXE padded.{TextColors.ENDC}")

def pump_mode_5(file, size):
    with open(file, 'ab') as f:
        f.write(os.urandom(size))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 5: Reserved mode.{TextColors.ENDC}")

def pump_mode_6(file, size):
    with open(file, 'ab') as f:
        f.write(os.urandom(size))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 6: Generic fallback padded.{TextColors.ENDC}")

def pump_mode_7(file, size):
    with open(file, 'ab') as f:
        f.write(os.urandom(size))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 7: JSON/XML padded.{TextColors.ENDC}")

def pump_mode_8(file, size):
    with open(file, 'ab') as f:
        f.write(os.urandom(size))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 8: Database padded.{TextColors.ENDC}")

def pump_mode_9(file, size):
    with open(file, 'rb+') as f:
        content = f.read()
        eof_index = content.rfind(b'%%EOF')
        if eof_index != -1:
            f.seek(eof_index)
            f.write(b"\n% pumped comment\n")
            f.write(os.urandom(size - len(b"% pumped comment\n")))
            f.write(b"\n%%EOF")
        else:
            f.seek(0, os.SEEK_END)
            f.write(b"\n% pumped comment\n")
            f.write(os.urandom(size - len(b"% pumped comment\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 9: PDF padded with minimal corruption risk.{TextColors.ENDC}")

def pump_mode_10(file, size):
    with open(file, 'ab') as f:
        f.write(b"\n<!-- PUMPED -->\n")
        f.write(os.urandom(size - len(b"\n<!-- PUMPED -->\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 10: Web format padded.{TextColors.ENDC}")

def pump_mode_11(file, size):
    with open(file, 'ab') as f:
        f.write(b"<!--x:pumpx-->")
        f.write(os.urandom(size - len(b"<!--x:pumpx-->")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 11: Office doc padded safely.{TextColors.ENDC}")

def pump_mode_12(file, size):
    with open(file, 'ab') as f:
        f.write(b"# padding ")
        f.write(os.urandom(size - len(b"# padding ")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 12: Torrent padded.{TextColors.ENDC}")

def pump_mode_13(file, size):
    with open(file, 'ab') as f:
        f.write(b"\0" * size)
    print(f"{TextColors.BACKGROUND_GREEN}Mode 13: Font padded.{TextColors.ENDC}")

def pump_mode_14(file, size):
    with open(file, 'ab') as f:
        f.write(b"\n<!-- PADDING -->\n")
        f.write(os.urandom(size - len(b"\n<!-- PADDING -->\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 14: Markdown padded.{TextColors.ENDC}")

def pump_mode_15(file, size):
    with open(file, 'ab') as f:
        f.write(b"\n# PADDING\n")
        f.write(os.urandom(size - len(b"\n# PADDING\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 15: Shell script padded.{TextColors.ENDC}")

def pump_mode_16(file, size):
    with open(file, 'ab') as f:
        f.write(b"\n<!-- epub-padded -->\n")
        f.write(os.urandom(size - len(b"\n<!-- epub-padded -->\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 16: EPUB padded.{TextColors.ENDC}")

def pump_mode_17(file, size):
    with open(file, 'ab') as f:
        f.write(b"-- SQLite padded --\n")
        f.write(os.urandom(size - len(b"-- SQLite padded --\n")))
    print(f"{TextColors.BACKGROUND_GREEN}Mode 17: SQLite-specific padded.{TextColors.ENDC}")


def pump_mode_99(file, size):
    if current_performance_mode == PerformanceMode.AGGRESSIVE:
        def aggressive_writer(f, chunk):
            f.write(bytearray(random.getrandbits(8) for _ in range(chunk)))
        threaded_pump(file, size, aggressive_writer)
    else:
        with open(file, 'ab') as f:
            written = 0
            chunk_size = get_chunk_size(size)
            while written < size:
                current_chunk = min(chunk_size, size - written)
                if current_performance_mode == PerformanceMode.LOW:
                    f.write(os.urandom(current_chunk))
                else:
                    f.write(bytearray(random.getrandbits(8) for _ in range(current_chunk)))
                written += current_chunk
    
    print(f"{TextColors.BACKGROUND_GREEN}Mode 99: Pumping complete ({size} bytes){TextColors.ENDC}")



def preview_file(file, added_size):
    original = os.path.getsize(file)
    print(f"{TextColors.ORANGE}Preview: Original size = {original} bytes, After = {original + added_size} bytes{TextColors.ENDC}")

def check_integrity(file):
    print(f"{TextColors.CYAN}Checking file integrity for: {file}{TextColors.ENDC}")
    if shutil.which('file'):
        os.system(f"file '{file}'")
    else:
        print(f"{TextColors.ORANGE}No integrity checker available.{TextColors.ENDC}")

def add_file_data(file, size, mode, extra=None):
    modes = {
        1: pump_mode_1, 2: pump_mode_2, 3: pump_mode_3, 4: pump_mode_4,
        5: pump_mode_5, 6: pump_mode_6, 7: pump_mode_7, 8: pump_mode_8,
        9: pump_mode_9, 10: pump_mode_10, 11: pump_mode_11, 12: pump_mode_12,
        13: pump_mode_13, 14: pump_mode_14, 15: pump_mode_15,
        16: pump_mode_16, 17: pump_mode_17, 99: pump_mode_99,
    }
    if mode not in modes:
        print(f"{TextColors.RED}Unknown mode selected!{TextColors.ENDC}")
        return
    modes[mode](file, size)

def main():
    print_logo()
    print_performance_modes()
    
    try:
        auto_detect_mode()
        
        files = input("\nEnter file paths (comma separated): ").split(',')
        file_size = input("Amount to add (e.g., '100KB', '5MB'): ")
        validate_file_size(file_size)
        size_in_bytes = parse_size(file_size)
        confirm_large_addition(size_in_bytes)

        print_pump_modes()
        mode_input = input("\nSelect pumping mode (leave empty for auto): ")
        preview = input("Preview file size first? (y/n): ").lower() == 'y'
        check = input("Check file integrity after? (y/n): ").lower() == 'y'

        for file in files:
            file = file.strip()
            validate_file_path(file)
            mode = int(mode_input) if mode_input.strip() else get_extension_mode(file)
            print(f"\n{TextColors.ORANGE}Pumping: {file} using mode {mode}{TextColors.ENDC}")
            if preview: preview_file(file, size_in_bytes)
            add_file_data(file, size_in_bytes, mode)
            if check: check_integrity(file)
            check_writable(file)
            check_disk_space(file, size_in_bytes + 4096)

    except Exception as e:
        print(f"\n{TextColors.BACKGROUND_RED}Error: {e}{TextColors.ENDC}")

if __name__ == "__main__":
    main()
