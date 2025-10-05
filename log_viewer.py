#!/usr/bin/env python3
"""
Log utility for FightBot - helps view and manage debate logs.
"""

import os
import tempfile
import glob
import logging
from datetime import datetime
import argparse

def find_fightbot_logs():
    """Find all FightBot log directories and files."""
    temp_dir = tempfile.gettempdir()
    
    # Find debate log directories
    debate_dirs = glob.glob(os.path.join(temp_dir, "fightbot_debate_*"))
    
    # Find file-based bot log directories  
    filebot_dirs = glob.glob(os.path.join(temp_dir, "chatfile_bot_*"))
    
    return debate_dirs + filebot_dirs

def list_logs():
    """List all available FightBot logs."""
    print("=== FightBot Log Files ===\n")
    
    log_dirs = find_fightbot_logs()
    
    if not log_dirs:
        print("No FightBot log files found.")
        return []
    
    all_logs = []
    
    for log_dir in sorted(log_dirs, key=os.path.getmtime, reverse=True):
        # Get creation time
        create_time = datetime.fromtimestamp(os.path.getmtime(log_dir))
        
        # Find log files in directory
        log_files = glob.glob(os.path.join(log_dir, "*.log"))
        
        if log_files:
            for log_file in log_files:
                file_size = os.path.getsize(log_file)
                file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                
                log_info = {
                    'path': log_file,
                    'size': file_size,
                    'time': file_time,
                    'type': 'debate' if 'fightbot_debate' in log_dir else 'filebot'
                }
                all_logs.append(log_info)
    
    # Sort by time, newest first
    all_logs.sort(key=lambda x: x['time'], reverse=True)
    
    # Display logs
    for i, log_info in enumerate(all_logs, 1):
        log_type = log_info['type'].upper()
        size_kb = log_info['size'] / 1024
        time_str = log_info['time'].strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{i:2d}. [{log_type}] {time_str} ({size_kb:.1f} KB)")
        print(f"    {log_info['path']}")
        print()
    
    return all_logs

def view_log(log_path, lines=None, tail=False):
    """View contents of a log file."""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        if not content:
            print("Log file is empty.")
            return
        
        print(f"=== Log File: {os.path.basename(log_path)} ===")
        print(f"Total lines: {len(content)}\n")
        
        if tail and lines:
            # Show last N lines
            content = content[-lines:]
            print(f"[Showing last {lines} lines]\n")
        elif lines:
            # Show first N lines
            content = content[:lines]
            print(f"[Showing first {lines} lines]\n")
        
        for i, line in enumerate(content, 1):
            print(f"{i:4d}: {line.rstrip()}")
            
    except Exception as e:
        print(f"Error reading log file: {e}")

def search_logs(search_term):
    """Search for specific terms in log files."""
    print(f"=== Searching for '{search_term}' in FightBot logs ===\n")
    
    log_dirs = find_fightbot_logs()
    found_matches = False
    
    for log_dir in log_dirs:
        log_files = glob.glob(os.path.join(log_dir, "*.log"))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                matches = []
                for line_num, line in enumerate(lines, 1):
                    if search_term.lower() in line.lower():
                        matches.append((line_num, line.strip()))
                
                if matches:
                    found_matches = True
                    print(f"File: {log_file}")
                    print(f"Found {len(matches)} matches:")
                    
                    for line_num, line in matches[:5]:  # Show first 5 matches
                        print(f"  {line_num:4d}: {line}")
                    
                    if len(matches) > 5:
                        print(f"  ... and {len(matches) - 5} more matches")
                    print()
                    
            except Exception as e:
                print(f"Error searching {log_file}: {e}")
    
    if not found_matches:
        print("No matches found.")

def cleanup_logs(days_old=7):
    """Remove log files older than specified days."""
    import time
    
    current_time = time.time()
    cutoff_time = current_time - (days_old * 24 * 60 * 60)
    
    log_dirs = find_fightbot_logs()
    removed_count = 0
    
    print(f"Cleaning up log files older than {days_old} days...")
    
    for log_dir in log_dirs:
        dir_time = os.path.getmtime(log_dir)
        
        if dir_time < cutoff_time:
            try:
                # Remove all files in directory
                log_files = glob.glob(os.path.join(log_dir, "*"))
                for log_file in log_files:
                    os.remove(log_file)
                    removed_count += 1
                
                # Remove directory
                os.rmdir(log_dir)
                print(f"Removed: {log_dir}")
                
            except Exception as e:
                print(f"Error removing {log_dir}: {e}")
    
    print(f"Cleanup complete. Removed {removed_count} files.")

def main():
    parser = argparse.ArgumentParser(description="FightBot Log Utility")
    parser.add_argument("command", choices=["list", "view", "search", "cleanup"], 
                       help="Command to execute")
    parser.add_argument("--index", type=int, help="Log index to view (from list command)")
    parser.add_argument("--path", help="Direct path to log file")
    parser.add_argument("--lines", type=int, help="Number of lines to show")
    parser.add_argument("--tail", action="store_true", help="Show last N lines instead of first")
    parser.add_argument("--term", help="Search term for search command")
    parser.add_argument("--days", type=int, default=7, help="Days old for cleanup (default: 7)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_logs()
    
    elif args.command == "view":
        if args.path:
            view_log(args.path, args.lines, args.tail)
        elif args.index:
            logs = list_logs()
            if logs and 1 <= args.index <= len(logs):
                log_path = logs[args.index - 1]['path']
                view_log(log_path, args.lines, args.tail)
            else:
                print(f"Invalid log index: {args.index}")
        else:
            print("Use --index or --path to specify which log to view")
    
    elif args.command == "search":
        if args.term:
            search_logs(args.term)
        else:
            print("Use --term to specify search term")
    
    elif args.command == "cleanup":
        cleanup_logs(args.days)

if __name__ == "__main__":
    main()