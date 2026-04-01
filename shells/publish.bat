@echo off

rd /s /q public\\extends
rd /s /q public\\publish
rd /s /q public\\publish-zip
mkdir public\\publish-zip


cd fnpackup.web
call npm install
call npm run build
cd ../


for %%r in (win-x86,win-x64,win-arm64) do (
	
	dotnet publish fnpackup -c release -f net8.0 -o public/publish/%%r/fnpackup-%%r  -r %%r  -p:PublishSingleFile=true  --self-contained true  -p:TrimMode=partial -p:TieredPGO=true  -p:DebugType=full -p:EventSourceSupport=false -p:DebugSymbols=true -p:EnableCompressionInSingleFile=true -p:DebuggerSupport=false -p:EnableUnsafeBinaryFormatterSerialization=false -p:EnableUnsafeUTF7Encoding=false -p:HttpActivityPropagationSupport=false -p:InvariantGlobalization=true  -p:MetadataUpdaterSupport=false  -p:UseSystemResourceKeys=true -p:MetricsSupport=false -p:StackTraceSupport=false -p:XmlResolverIsNetworkingEnabledByDefault=false
	echo F|xcopy "public\\extends\\%%r\\fnpackup-%%r\\*" "public\\publish\\%%r\\fnpackup-%%r\\*"  /s /f /h /y

	echo F|xcopy "public\\extends\\any\\*" "public\\publish\\%%r\\fnpackup-%%r\\*"  /s /f /h /y
	echo F|xcopy "fnpackup.tray\\dist\\*" "public\\publish\\%%r\\fnpackup-%%r\\*"  /s /f /h /y

    del /q /f /s "public\\publish\\%%r\\fnpackup-%%r\\fnpackup.staticwebassets.endpoints.json"
    del /q /f /s "public\\publish\\%%r\\fnpackup-%%r\\aspnetcorev2_inprocess.dll"

	7z a -tzip ./public/publish-zip/fnpackup-%%r.zip ./public/publish/%%r/*
)