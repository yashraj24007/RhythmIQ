@REM ----------------------------------------------------------------------------
@REM Licensed to the Apache Software Foundation (ASF) under one
@REM or more contributor license agreements.  See the NOTICE file
@REM distributed with this work for additional information
@REM regarding copyright ownership.  The ASF licenses this file
@REM to you under the Apache License, Version 2.0 (the
@REM "License"); you may not use this file except in compliance
@REM with the License.  You may obtain a copy of the License at
@REM
@REM    https://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing,
@REM software distributed under the License is distributed on an
@REM "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
@REM KIND, either express or implied.  See the License for the
@REM specific language governing permissions and limitations
@REM under the License.
@REM ----------------------------------------------------------------------------

@REM ----------------------------------------------------------------------------
@REM Apache Maven Wrapper startup batch script, version 3.3.2
@REM
@REM Optional ENV vars
@REM   MVNW_REPOURL - repo url base for downloading maven distribution
@REM   MVNW_USERNAME/MVNW_PASSWORD - user and password for downloading maven
@REM   MVNW_VERBOSE - true: enable verbose log; others: silence the output
@REM ----------------------------------------------------------------------------

@IF "%DEBUG%"=="" @ECHO OFF
@REM set title of command window
title %0
@REM enable echoing my setting MAVEN_BATCH_ECHO to 'on'
@IF "%MAVEN_BATCH_ECHO%"=="on"  ECHO %MAVEN_BATCH_ECHO%

@REM set %HOME% to equivalent of $HOME
if "%HOME%"=="" (set "HOME=%HOMEDRIVE%%HOMEPATH%")

@REM Execute a user defined script before this one
if not "%MVNW_PRE_CMD%"=="" call "%MVNW_PRE_CMD%"
@setlocal

set ERROR_CODE=0

@REM To isolate internal variables from possible post scripts, we use another setlocal
@setlocal

@REM ==== START VALIDATION ==== 
if not "%JAVA_HOME%"=="" goto OkJHome

@REM Attempt to auto-detect JAVA_HOME from java on PATH if not explicitly set
for /f "delims=" %%i in ('where java 2^>NUL') do (
	set "JAVA_EXE=%%i"
	@REM Strip the trailing \bin\java.exe -> go up one directory to get JAVA_HOME
	set "JAVA_HOME=%%~dpi.."
	echo Detected JAVA_HOME from PATH: %JAVA_HOME%
	goto OkJHome
)

@REM If we reach here, java.exe not found on PATH. Attempt lightweight JDK bootstrap.
echo JAVA_HOME not set and no system java found. Attempting to download JDK 21 locally...
set "JDK_BOOT_DIR=%USERPROFILE%\.jdks"
if not exist "%JDK_BOOT_DIR%" mkdir "%JDK_BOOT_DIR%"
pushd "%JDK_BOOT_DIR%"
set "JDK_ZIP_URL=https://aka.ms/download-jdk/microsoft-jdk-21-windows-x64.zip"
set "JDK_ZIP_FILE=microsoft-jdk-21-win-x64.zip"
if not exist "%JDK_ZIP_FILE%" (
	powershell -Command "try { Invoke-WebRequest -Uri %JDK_ZIP_URL% -OutFile %JDK_ZIP_FILE% -UseBasicParsing } catch { exit 1 }"
)
if exist "%JDK_ZIP_FILE%" (
	powershell -Command "Try { Expand-Archive -Path '%JDK_ZIP_FILE%' -DestinationPath '.' -Force } Catch { exit 1 }"
	for /d %%d in ("%JDK_BOOT_DIR%\microsoft-jdk-21*") do set "JAVA_HOME=%%d"
	if not "%JAVA_HOME%"=="" (
		echo Bootstrapped local JDK at %JAVA_HOME%
		popd
		goto OkJHome
	) else (
		echo Failed to identify extracted JDK directory. >&2
		popd
		goto jdkFailure
	)
) else (
	echo Failed to download JDK archive. >&2
	popd
	goto jdkFailure
)

:jdkFailure
echo.
echo Error: JAVA_HOME not found and automatic JDK download failed. >&2
echo Please install a JDK (21+) and set JAVA_HOME manually. >&2
echo (Example)  setx JAVA_HOME "C:\\Program Files\\Java\\jdk-21" /M  (then reopen shell) >&2
echo.
goto error

:OkJHome
if exist "%JAVA_HOME%\bin\java.exe" goto init

echo.
echo Error: JAVA_HOME is set to an invalid directory. >&2
echo JAVA_HOME = "%JAVA_HOME%" >&2
echo Attempting secondary scan for installed JDKs... >&2

for %%d in ("C:\\Program Files\\Java" "C:\\Program Files\\Eclipse Adoptium" "C:\\Program Files\\Microsoft" "C:\\Program Files\\Zulu" ) do (
	if exist %%d (
		for /f "delims=" %%j in ('dir /b /ad "%%d" ^| findstr /r /c:"jdk" /c:"java"') do (
			if exist "%%d\%%j\bin\java.exe" (
				set "JAVA_HOME=%%d\%%j"
				echo Found candidate JDK at %JAVA_HOME%
				if exist "%JAVA_HOME%\bin\java.exe" goto init
			)
		)
	)
)

echo No valid JDK found via automatic scan. >&2
echo Please set the JAVA_HOME variable in your environment to match the >&2
echo location of your Java installation. Example (PowerShell as Admin): >&2
echo   winget install --id Microsoft.OpenJDK.21 -e >&2
echo   setx JAVA_HOME "C:\\Program Files\\Microsoft\\jdk-21" /M >&2
echo Then reopen the terminal and re-run mvnw.cmd. >&2
echo.
goto error

@REM ==== END VALIDATION ==== 

:init

set MAVEN_CMD_LINE_ARGS=%*

@REM Derive project base dir to satisfy multiModuleProjectDirectory requirement
set PROJECT_DIR=%~dp0
for %%i in ("%PROJECT_DIR%.") do set MAVEN_PROJECTBASEDIR=%%~fi
set MAVEN_CMD_LINE_ARGS=-Dmaven.multiModuleProjectDirectory=%MAVEN_PROJECTBASEDIR% %MAVEN_CMD_LINE_ARGS%

set DOWNLOAD_URL="https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.6/apache-maven-3.9.6-bin.zip"
set DOWNLOAD_DIR=%USERPROFILE%\.m2\wrapper\dists
set DOWNLOAD_PATH=%DOWNLOAD_DIR%\apache-maven-3.9.6-bin.zip
set MAVEN_HOME=%DOWNLOAD_DIR%\apache-maven-3.9.6

if exist "%MAVEN_HOME%" goto runmvn

if not exist "%DOWNLOAD_DIR%" md "%DOWNLOAD_DIR%"
echo Downloading Maven 3.9.6...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('%DOWNLOAD_URL%', '%DOWNLOAD_PATH%')"
tar -xf "%DOWNLOAD_PATH%" -C "%DOWNLOAD_DIR%"

:runmvn
set MAVEN_JAVA_EXE="%JAVA_HOME%\bin\java.exe"
set WRAPPER_JAR="%~dp0\.mvn\wrapper\maven-wrapper.jar"
set WRAPPER_LAUNCHER=org.apache.maven.wrapper.MavenWrapperMain

%MAVEN_JAVA_EXE% %MAVEN_OPTS% -classpath %WRAPPER_JAR% %WRAPPER_LAUNCHER% %MAVEN_CMD_LINE_ARGS%
if ERRORLEVEL 1 goto error
goto end

:error
set ERROR_CODE=1

:end
@endlocal & set ERROR_CODE=%ERROR_CODE%
if not "%MVNW_POST_CMD%"=="" call "%MVNW_POST_CMD%"
if %ERROR_CODE%==0 (exit /b 0) else (exit /b %ERROR_CODE%)
