#!/bin/bash

# Get current path
CURRENT_PATH=$(pwd)

# Create a single script with all the commands
osascript <<EOF
tell application "Terminal"
    -- Execute first command in the current tab
    do script "cd $CURRENT_PATH/backend && source .venv/bin/activate && python main.py"
    
    -- Create a new tab for the admin service
    tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
    delay 0.5
    do script "cd $CURRENT_PATH/admin && source .venv/bin/activate && python main.py" in front window
    
    -- Create a new tab for the frontend service
    tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
    delay 0.5
    do script "cd $CURRENT_PATH/frontend && bun run dev" in front window
end tell
EOF