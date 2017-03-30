set p1 to (POSIX path of (POSIX file (do shell script "pwd"))) & "/ovpn"
set p2 to POSIX file p1
#display dialog p2
tell application "Finder" to open every file of folder (p2) using ((path to applications folder as text) & "Tunnelblick.app")
