$scriptpath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptpath
Write-host "My directory is $dir"
cd $dir
cd "Elastic Beanstalk\GestureRec"
dir
.\Scripts\activate
Python "application.py"
pause