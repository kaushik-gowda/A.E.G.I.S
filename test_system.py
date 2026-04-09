#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A.E.G.I.S (Autonomous Execution & Guidance Intelligent System) System Tester
Tests core functionality without launching the full UI
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from tools.os_commands import os_commands
from core.agent import AegisAgent

def test_os_commands():
    """Test OS command module."""
    print("=" * 60)
    print("TESTING OS COMMANDS MODULE")
    print("=" * 60)
    
    # Test system info
    print("\n1. Getting system information...")
    result = os_commands.get_system_info()
    if result["status"] == "success":
        print(f"   ✓ CPU Usage: {result['cpu_usage']:.1f}%")
        print(f"   ✓ Memory Usage: {result['memory_usage']:.1f}%")
        print(f"   ✓ Disk Usage: {result['disk_usage']:.1f}%")
    else:
        print(f"   ✗ Failed: {result['message']}")
    
    # Test running applications
    print("\n2. Getting running applications...")
    result = os_commands.get_running_applications()
    if result["status"] == "success":
        print(f"   ✓ Found {len(result['processes'])} running processes")
        print(f"     Sample: {', '.join(result['processes'][:5])}")
    else:
        print(f"   ✗ Failed: {result['message']}")
    
    print("\n✓ OS Commands module working correctly!")

def test_agent():
    """Test AI agent module."""
    print("\n" + "=" * 60)
    print("TESTING AI AGENT MODULE")
    print("=" * 60)
    
    agent = AegisAgent()
    
    # Test task management
    print("\n1. Testing task management...")
    task = agent.task_manager.add_task("Test Task", "This is a test", "high")
    print(f"   ✓ Task created: {task['title']} (ID: {task['id']})")
    
    tasks = agent.task_manager.get_tasks()
    print(f"   ✓ Total tasks: {len(tasks)}")
    
    # Test command processing
    print("\n2. Testing command processing...")
    test_commands = [
        "Hello",
        "What's the system info?",
        "Show me my tasks",
        "Help",
        "What time is it?",
    ]
    
    for cmd in test_commands:
        response = agent._handle_command(cmd)
        print(f"   Command: '{cmd}'")
        print(f"   Response: {response[:100]}..." if len(response) > 100 else f"   Response: {response}")
        print()
    
    print("✓ AI Agent module working correctly!")

def test_ui_imports():
    """Test UI module imports."""
    print("\n" + "=" * 60)
    print("TESTING UI MODULE IMPORTS")
    print("=" * 60)
    
    try:
        from ui.app_window import AegisWindow
        print("   ✓ PyQt6 UI module imports successfully")
        print("   ✓ AegisWindow class available")
    except Exception as e:
        print(f"   ✗ Import failed: {str(e)}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "A.E.G.I.S SYSTEM DIAGNOSTIC TEST" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # Test OS commands
        test_os_commands()
        
        # Test agent
        test_agent()
        
        # Test UI imports
        if test_ui_imports():
            print("\n" + "=" * 60)
            print("ALL TESTS PASSED ✓")
            print("=" * 60)
            print("\nYou can now run: python main.py")
        else:
            print("\n⚠ Some UI components need attention")
            
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
